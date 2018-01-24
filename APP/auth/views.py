# coding: utf-8
from . import auth_option
from sqlalchemy import and_
from flask import *
from .forms import AddProject, ProjectMange, ProjectAPIMag, addProjectAPI, ApiCaseMange, addApiCase, EditProjectForm, EditAPIForm, \
    EditApiCase, RunMange, AddRunMange, EditRunMange, SortCase, SortApi, AddRunApi, DebugCaseForm, ConfigMange, \
    AddConfig, EditConfigForm, SetupTearDownForm, SearchSetupTearDownForm, EditSetupTearDownForm
from ..models import Project, ProjectAPI, APICase, RunCaseConfig, CaseSort, ConfigParse, StepTearDown, APSCheduler, CaseResult
from .. import db
from ..RunCase.runcase import RunCase
from ..RunCase.common.readlogfile import log_file
from ..RunCase.common.mydb import MyDb
import datetime
from pygal.style import DefaultStyle
import pygal
from .. import scheduler
import os
import time
from config import *
@auth_option.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))
    #basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    db_con = MyDb(os.path.join(basedir, 'jobs.sqlite'), 'sqlite')
    aps_time_sql ='select id,next_run_time from apscheduler_jobs'
    aps_times = db_con.select_many_record(aps_time_sql)

    aps_time_infos = []
    if aps_times:
        for aps_time in aps_times:
            aps_info = {}
            run_case_config =RunCaseConfig.query.filter_by(id=int(aps_time[0])).first()
            project_info = Project.query.filter_by(id=run_case_config.project_id).first()

            aps_info['name'] = project_info.name + '_' + run_case_config.plan_name
            aps_info['next_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(aps_time[1])))

            aps_time_infos.append(aps_info)

    projects = Project.query.all()
    projectapis = ProjectAPI.query.all()
    cases = APICase.query.all()
    aps_cases = APSCheduler.query.all()


    run_batch = []
    case_results = CaseResult.query.all()
    # max_run_batch = CaseResult.query(func.max(CaseResult.run_batch)).first()
    fail_count_list = [None]
    pass_count_list = [None]
    for case_result in case_results:
        if case_result.run_batch not in run_batch:
            fail_count = CaseResult.query.filter_by(run_batch=case_result.run_batch, run_result='fail').count()
            pass_count = CaseResult.query.filter_by(run_batch=case_result.run_batch, run_result='success').count()
            run_batch.append(int(case_result.run_batch))
            fail_count_list.append(fail_count)
            pass_count_list.append(pass_count)
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle, height=200)
    line_chart.title = '各批次运行情况'
    if run_batch:
        line_chart.x_labels = map(str, range(0, max(run_batch)+1))
    else:
        line_chart.x_labels = map(str, range(0, 0))
    line_chart.add('FAIL', fail_count_list)
    line_chart.add('SUCCESS', pass_count_list)

    project_cases = []
    for project in projects:
        project_count = APICase.query.filter_by(project_id=project.id).count()
        project_cases.append((project.name, project_count))
    pie_chart = pygal.Pie(height=200)
    pie_chart.title = '用例分布图'
    for project_case in project_cases:
        pie_chart.add(project_case[0], project_case[1])
    # line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])

    # line_chart.render_to_file('bar_chart.svg')




    return render_template("index.html", len_pro=len(projects), len_api=len(projectapis), len_case=len(cases),
                           len_aps=len(aps_times), aps_times=aps_time_infos, chart=line_chart, pie_chart=pie_chart)

@auth_option.route('/add/project', methods=['GET', 'POST'])
def add_project():
    form2 = AddProject()
    if request.method == 'POST':
        project_option = Project.query.filter_by(name=form2.project_name.data).first()
        if project_option:
            flash(u'添加项目失败！该项目名称已经存在。', 'danger')
        else:
            try:
                # url=form2.project_url.data,
                project_api = Project(name=form2.project_name.data,
                                      desc=form2.project_remark.data,
                                      project_status=form2.is_valid.data, Operator_name=session['username'])
                db.session.add(project_api)
                db.session.commit()
                flash(u'添加项目成功成功！', 'success')
            except:
                flash(u'操作异常，请稍后重试', 'danger')
        return redirect(url_for('.project_mange', form2=form2))
@auth_option.route('/project/mange', methods=['GET', 'POST'])
def project_mange():
    case_id = request.args.get('project_id', -1, type=int)  # 项目ID
    case_ids = APICase.return_project()
    case_ids.append(('-1', u'无'))
    form = ProjectMange()
    form2 = AddProject()
    form3 = addProjectAPI()
    form4 = EditProjectForm()
    form5 = SetupTearDownForm(relay_id=case_id)
    projects = Project.return_project()
    form3.project_id.choices = projects
    form5.relay_id.choices = case_ids
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))

    projects = Project.query.order_by(Project.id.desc()).all()

    if request.method == 'POST':
        projects = Project.query.filter_by(name=form.project_name.data).all()
        if len(projects) == 0:
            flash(u'根据项目名称:{0}未查出相关项目信息'.format(form.project_name.data), 'danger')
        else:
            return render_template("projectmanage.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, len_projects=len(projects), projects=projects)

    return render_template("projectmanage.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, len_projects=len(projects), projects=projects)

@auth_option.route('/project/editmange', methods=['GET', 'POST'])
def editproject_mange():
    form4 = EditProjectForm()

    if 'username' not in session:
        return redirect(url_for("auth_login.login"))

    if request.method == 'POST':
        name = form4.project_name.data
        project_id = int(form4.project_id.data)
        if Project.query.filter_by(name=name).first() \
            and Project.query.filter_by(name=name).first().id != project_id:
            flash(u'添加项目失败！存在多个项目名称。', 'danger')
        else:
            project = Project.query.get_or_404(project_id)
            try:

                project.name=form4.project_name.data
                # project.url = form4.project_url.data
                project.desc = form4.project_remark.data
                project.project_status = form4.is_valid.data
                project.Operator_name = session['username']
                db.session.add(project)
                db.session.commit()
                flash(u'修改项目信息成功！', 'success')
            except:
                flash(u'操作异常，请稍后重试', 'danger')

    return redirect(url_for('.project_mange', form4=form4))

@auth_option.route('/projectapi/mange/<string:id>', methods=['GET', 'POST'])
def projectAPI_mange(id):
    project_id = request.args.get('project_id', int(id), type=int)  # 项目ID
    apis_id = request.args.get('api_id', -1, type=int)  # 接口id
    case_id = request.args.get('rely_id', -1, type=int)  # 接口id
    form = ProjectAPIMag(project_id=project_id)
    form2 = addProjectAPI(project_id=project_id)
    form3 = addApiCase(project_id=project_id, api_id=apis_id)
    form4 = EditAPIForm()
    form5 = SetupTearDownForm(rely_id=case_id)
    projects = Project.return_project()
    projects.append(('-1', u'全部'))
    form2.project_id.choices = projects
    form.project_id.choices = projects
    form3.project_id.choices = projects
    form4.project_id.choices = projects
    projectapi = ProjectAPI.return_project()
    projectapi.append(('-1', u'全部'))
    form3.api_id.choices = projectapi
    apicaseid = [(m.id, m.case_name) for m in APICase.query.filter_by(project_id=project_id)]
    apicaseid.append(('-1', u'无'))
    # rely_case_ids.append(('-1', u'无'))
    form5.relay_id.choices = apicaseid
    page = request.args.get('page', 1, type=int)
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))

    if id == '-1':
        pagination = ProjectAPI.query.order_by(ProjectAPI.id.desc()).paginate(
            page, per_page=current_app.config['COMMENTS_PER_PAGE'],
            error_out=False)

        projectapis = pagination.items
        # projectapis = ProjectAPI.query.order_by(ProjectAPI.id.desc()).all()
    else:
        pagination = ProjectAPI.query.filter_by(project_id=form.project_id.data).paginate(
            page, per_page=current_app.config['COMMENTS_PER_PAGE'],
            error_out=False)

        projectapis = pagination.items
        # projectapis = ProjectAPI.query.filter_by(project_id=form.project_id.data).all()
    if request.method == 'POST':
        if form.project_id.data == -1 and form.api_name.data:
            pagination = ProjectAPI.query.filter_by(api_name=form.api_name.data).paginate(
                page, per_page=current_app.config['COMMENTS_PER_PAGE'],
                error_out=False)

            projectapis = pagination.items


            # projectapis = ProjectAPI.query.filter_by(api_name=form.api_name.data).all()
            if len(projectapis) == 0:
                flash(u'根据接口名称:{0}未查出相关项目信息'.format(form.api_name.data), 'danger')
            else:
                return render_template("projectapimanage.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, len_projectapis=len(projectapis),
                                   projectapis=projectapis, project=Project, project_id=form.project_id.data,
                                   pagination=pagination, endpoint='.projectAPI_mange', page=page)


        elif form.project_id.data == -1 and request.args.get('api_name') is None:
            pagination = ProjectAPI.query.order_by(ProjectAPI.id.desc()).paginate(
                page, per_page=current_app.config['COMMENTS_PER_PAGE'],
                error_out=False)

            projectapis = pagination.items

            # projectapis = ProjectAPI.query.order_by(ProjectAPI.id.desc()).all()
            if len(projectapis) == 0:
                flash(u'根据接口名称:{0}未查出相关项目信息'.format(form.api_name.data), 'danger')
            else:
                return render_template("projectapimanage.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5,
                len_projectapis=len(projectapis), projectapis=projectapis, project=Project, project_id=form.project_id.data,
                pagination=pagination, endpoint='.projectAPI_mange', page=page)

        elif form.api_name.data and form.project_id.data != -1:
            pagination = ProjectAPI.query.filter_by(project_id=form.project_id.data, api_name=form.api_name.data).paginate(
                page, per_page=current_app.config['COMMENTS_PER_PAGE'],
                error_out=False)

            projectapis = pagination.items


            #projectapis = ProjectAPI.query.filter_by(project_id=form.project_id.data, api_name=form.api_name.data).all()
            if len(projectapis) == 0:
                flash(u'根据接口名称:{0}未查出相关项目信息'.format(form.api_name.data), 'danger')
            else:
                return render_template("projectapimanage.html", form=form, form2=form2, form3=form3,
                                       form4=form4, form5=form5, len_projectapis=len(projectapis),
                           projectapis=projectapis, project=Project, project_id=form.project_id.data,
                                       pagination=pagination, endpoint='.projectAPI_mange', page=page)
        else:

            pagination = ProjectAPI.query.filter_by(project_id=form.project_id.data).paginate(
                page, per_page=current_app.config['COMMENTS_PER_PAGE'],
                error_out=False)

            projectapis = pagination.items
            # projectapis = ProjectAPI.query.filter_by(project_id=form.project_id.data).all()
            if len(projectapis) == 0:
                flash(u'根据接口名称:{0}未查出相关项目信息'.format(form.api_name.data), 'danger')
            else:
                return render_template("projectapimanage.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5,
                               len_projectapis=len(projectapis),
                               projectapis=projectapis, project=Project, project_id=form.project_id.data, pagination=pagination, endpoint='.projectAPI_mange', page=page)

    return render_template("projectapimanage.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, len_projectapis=len(projectapis), projectapis=projectapis,
                           project=Project, project_id=form.project_id.data, pagination=pagination, endpoint='.projectAPI_mange', page=page)

@auth_option.route('/add/projectapi', methods=['GET', 'POST'])
def add_projectapi():
    form2 = addProjectAPI()
    if request.method == 'POST':
        api_option = ProjectAPI.query.filter_by(api_name=form2.api_name.data, project_id=form2.project_id.data).first()
        if api_option:
            flash(u'添加接口失败！该项目下该接口名称已经存在。', 'danger')
        else:
            try:
                project_api = ProjectAPI(api_name=form2.api_name.data, api_url=form2.api_url.data, api_heard=form2.api_heard.data,
                                      api_resp=form2.api_resp.data, api_req=form2.api_req.data, api_method=form2.api_method.data,
                                      project_id=form2.project_id.data,
                                      api_status=form2.api_valid.data, Operator_name=session['username'])
                db.session.add(project_api)
                db.session.commit()
                flash(u'添加接口成功！', 'success')
            except:
                flash(u'操作异常，请稍后重试', 'danger')
        return redirect(url_for('.projectAPI_mange', form2=form2, id=form2.project_id.data))

@auth_option.route('/add/api_by_projectid', methods=['GET', 'POST'])
def addapi_by_id():
    form3 = addProjectAPI()
    if request.method == 'POST':
        api_option = ProjectAPI.query.filter_by(api_name=form3.api_name.data, project_id=form3.project_id.data).first()
        if api_option:
            flash(u'添加接口失败！该项目下该接口名称已经存在。', 'danger')
        else:
            try:
                project_api = ProjectAPI(api_name=form3.api_name.data, api_url=form3.api_url.data, api_heard=form3.api_heard.data,
                                      api_resp=form3.api_resp.data, api_req=form3.api_req.data,api_method=form3.api_method.data,
                                      project_id=form3.project_id.data,
                                      api_status=form3.api_valid.data, Operator_name=session['username'])
                db.session.add(project_api)
                db.session.commit()
                flash(u'添加接口成功！', 'success')
            except:
                flash(u'操作异常，请稍后重试', 'danger')
        return redirect(url_for('.projectAPI_mange', id=form3.project_id.data))

@auth_option.route('/add/getprojectid/<int:id>', methods=['GET', 'POST'])
def getproject_by_id(id):
    if request.is_xhr:
        return jsonify({
            'project_id': id,
        })

@auth_option.route('/add/getprojectvalue/<int:id>', methods=['GET', 'POST'])
def get_project_by_id(id):
    project = Project.query.get_or_404(id)
    if request.is_xhr:
        return jsonify({
            'project_id': id,
            'project_name': project.name,
            # 'project_url': project.url,
            'Operator_name': project.Operator_name,
            'project_status': project.project_status,
            'project_remark':project.desc
        })

@auth_option.route('/api/editapi', methods=['GET', 'POST'])
def edit_api_mange():
    form4 = EditAPIForm()
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))
    if request.method == 'POST':
        name = form4.api_name.data
        api_id = int(form4.api_id.data)
        if ProjectAPI.query.filter_by(api_name=name).first() \
            and ProjectAPI.query.filter_by(api_name=name).first().id != api_id:
            flash(u'修改接口失败！存在多个相同名称。', 'danger')
        else:
            project_api = ProjectAPI.query.get_or_404(api_id)
            try:
                project_api.api_name = form4.api_name.data
                project_api.api_url = form4.api_url.data
                project_api.api_req = form4.api_req.data
                project_api.api_heard = form4.api_heard.data
                project_api.api_resp = form4.api_resp.data
                project_api.api_method = form4.api_method.data
                project_api.api_status = form4.api_valid.data
                project_api.project_id = form4.project_id.data
                db.session.add(project_api)
                db.session.commit()
                flash(u'修改接口信息成功！', 'success')
            except:
                flash(u'操作异常，请稍后重试', 'danger')

    return redirect(url_for('.projectAPI_mange', form4=form4, id=form4.project_id.data))


@auth_option.route('/apicase/mange/<string:id>/<string:project_id>', methods=['GET', 'POST'])
def apicase_mange(id, project_id):
    project_id = request.args.get('project_id', int(project_id), type=int)#项目ID
    apis_id = request.args.get('api_id', int(id), type=int)#接口id
    case_id = request.args.get('rely_id', -1, type=int)  # 接口id
    form = ApiCaseMange(project_id=project_id, api_id=apis_id)
    form2 = addApiCase(request.form, project_id=project_id, api_id=apis_id)
    form3 = EditApiCase()
    form4 = SortCase()
    form5 = SetupTearDownForm(rely_id=case_id)
    projects = Project.return_project()
    projects.append(('-1', u'全部'))
    form.project_id.choices = projects
    form2.project_id.choices = projects
    form3.project_id.choices = projects
    projectapi = ProjectAPI.return_project()
    projectapi.append(('-1', u'全部'))
    form.api_id.choices = projectapi
    form2.api_id.choices = projectapi
    form3.api_id.choices = projectapi
    apicaseid = [(m.id, m.case_name) for m in APICase.query.filter_by(project_id=project_id)]
    apicaseid.append(('-1', u'无'))

    # rely_case_ids.append(('-1', u'无'))
    form5.relay_id.choices = apicaseid
    page = request.args.get('page', 1, type=int)
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))
    if id == '-1' and str(project_id) == '-1':
        pagination = APICase.query.order_by(APICase.id.asc()).paginate(
            page, per_page=current_app.config['COMMENTS_PER_PAGE'],
            error_out=False)
        apicases = pagination.items
        # apicases = APICase.query.all()
    elif id == '-1' and str(project_id) != '-1':
        pagination = APICase.query.filter_by(project_id=str(project_id)).order_by(APICase.id.asc()).paginate(
            page, per_page=current_app.config['COMMENTS_PER_PAGE'],
            error_out=False)
        apicases = pagination.items

    elif id != '-1' and str(project_id) == '-1':
        pagination = APICase.query.filter_by(api_id=id).paginate(
            page, per_page=current_app.config['COMMENTS_PER_PAGE'],
            error_out=False)
        apicases = pagination.items

    else:
        pagination = APICase.query.filter_by(api_id=id, project_id=str(project_id)).paginate(
            page, per_page=current_app.config['COMMENTS_PER_PAGE'],
            error_out=False)
        apicases = pagination.items
        # apicases = APICase.query.filter_by(api_id=form.api_id.data).all()
    if request.method == 'POST':
        page = request.args.get('page', 1, type=int)
        if form.project_id.data == -1 and form.api_id.data == -1:
            pagination = APICase.query.order_by(APICase.id.asc()).paginate(
                page, per_page=current_app.config['COMMENTS_PER_PAGE'],
                error_out=False)
            # apicases = APICase.query.all()
        elif form.project_id.data != -1 and form.api_id.data == -1:
            pagination = APICase.query.filter_by(project_id=form.project_id.data).paginate(
                page, per_page=current_app.config['COMMENTS_PER_PAGE'],
                error_out=False)

            # apicases = APICase.query.filter_by(project_id=form.project_id.data).all()
        elif form.project_id.data == -1 and form.api_id.data != -1:
            pagination = APICase.query.filter_by(api_id=form.api_id.data).paginate(
                page, per_page=current_app.config['COMMENTS_PER_PAGE'],
                error_out=False)
            # apicases = APICase.query.filter_by(api_id=form.api_id.data).all()
        else:
            pagination = APICase.query.filter_by(api_id=form.api_id.data, project_id=form.project_id.data).paginate(
                page, per_page=current_app.config['COMMENTS_PER_PAGE'],
                error_out=False)
            # apicases = APICase.query.filter_by(api_id=form.api_id.data, project_id=form.project_id.data).all()
        apicases = pagination.items
        if len(apicases) == 0:
            flash(u'接口无用例信息,请修改条件查询', 'danger')
        else:
            return render_template("apicasemanage.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, len_apicases=len(apicases),
                                   apicases=apicases, projectapi=ProjectAPI, project=Project, APICase=APICase, pagination=pagination, endpoint='.apicase_mange', page=page, api_id=form.api_id.data, project_id=form.project_id.data)

    return render_template("apicasemanage.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, len_apicases=len(apicases),
                           apicases=apicases, projectapi=ProjectAPI, project=Project, APICase=APICase, pagination=pagination, endpoint='.apicase_mange', page=page, api_id=form.api_id.data, project_id=form.project_id.data)

@auth_option.route('/add/apicase', methods=['GET', 'POST'])
def add_apicase():
    form2 = addApiCase()
    if request.method == 'POST':
        case_option = APICase.query.filter_by(case_name=form2.case_name.data, api_id=form2.api_id.data, project_id=form2.project_id.data).first()
        if case_option:
            flash(u'添加用例失败！该接口下该用例名称已经存在。', 'danger')
        else:
            try:

                api_case = APICase(case_name=form2.case_name.data, case_req=form2.case_req.data,
                                   Extract_failed=form2.Extract_failed.data, case_status=form2.case_valid.data, api_id=form2.api_id.data,
                                      project_id=form2.project_id.data, expect_result=form2.expect_result.data,
                                   Operator_name=session['username'], case_desc=form2.case_desc.data)

                db.session.add(api_case)
                db.session.commit()
                flash(u'添加用例成功！', 'success')
            except Exception as e:
                flash(u'操作异常，请稍后重试, 错误信息：%s'%e, 'danger')
        return redirect(url_for('.apicase_mange', form2=form2, id=form2.api_id.data,project_id=form2.project_id.data))

@auth_option.route("/api/proapiid/<int:project_id>/<int:api_id>", methods=['GET', 'POST'])
def get_projectapi_id(project_id, api_id):

    if request.is_xhr:
        return jsonify({
            'project_id': project_id,
            'api_id': api_id
        })

@auth_option.route("/api/getapivalue/<int:api_id>", methods=['GET', 'POST'])
def get_api_value(api_id):
    projectapi = ProjectAPI.query.get_or_404(api_id)
    if request.is_xhr:
        return jsonify({
            'api_id': projectapi.id,
            'project_id': projectapi.project_id,
            'api_name': projectapi.api_name,
            'api_url': projectapi.api_url,
            'api_req': projectapi.api_req,
            'api_heard': projectapi.api_heard,
            'api_resp': projectapi.api_resp,
            'api_method': projectapi.api_method,
            'api_status': projectapi.api_status,
        })

@auth_option.route("/case/getcasevalue/<int:case_id>", methods=['GET', 'POST'])
def get_case_value(case_id):
    apicase = APICase.query.get_or_404(case_id)
    apis = ProjectAPI.query.filter_by(id=apicase.api_id).first()
    if request.is_xhr:

        if '{' in apicase.case_req and '}' in apicase.case_req:
            # case_req = dict(eval(self.gc.case_json['api_req']), **eval(case_req_new))
            if apis.api_req:
                case_req = dict(eval(apis.api_req), **eval(apicase.case_req))
                case_req_new = json.dumps(case_req)
            else:
                case_req = eval(apicase.case_req)
                case_req_new = json.dumps(case_req)
        else:
            case_req_new = apicase.case_req
        return jsonify({

            'case_id': apicase.id,
            'case_name': apicase.case_name,
            'case_desc': apicase.case_desc,
            'api_name': apis.api_name,
            'api_url': apis.api_url,
            'api_heard': apis.api_heard,
            'api_resp': apis.api_resp,
            'api_method': apis.api_method,
            'api_req': case_req_new,
            # 'rely_case_id': apicase.rely_case_id,
            'api_id': apicase.api_id,
            'project_id': apicase.project_id,
            'case_req': apicase.case_req,
            # 'case_head_add': apicase.case_head_add,
            'expect_result': apicase.expect_result,
            'Extract_failed': apicase.Extract_failed,
            'case_valid': apicase.case_status,
        })

@auth_option.route('/case/add_case_id/', methods=['GET', 'POST'])
def add_case_by_apiid():
    form3 = addApiCase()
    if request.method == 'POST':
        case_option = APICase.query.filter_by(case_name=form3.case_name.data, api_id=form3.api_id.data,
                                              project_id=form3.project_id.data).first()
        if case_option:
            flash(u'添加用例失败！该接口下该用例名称已经存在。', 'danger')
        else:
            try:
                api_case = APICase(case_name=form3.case_name.data, case_req=form3.case_req.data,
                                   Extract_failed=form3.Extract_failed.data, case_status=form3.case_valid.data,
                                   api_id=form3.api_id.data,
                                   project_id=form3.project_id.data, expect_result=form3.expect_result.data,
                                    Operator_name=session['username'],case_desc=form3.case_desc.data)

                db.session.add(api_case)
                db.session.commit()
                flash(u'添加用例成功！', 'success')
            except:
                flash(u'操作异常，请稍后重试', 'danger')
        return redirect(url_for('.apicase_mange', form3=form3, id=form3.api_id.data, project_id=form3.project_id.data))

@auth_option.route('/case/editcase', methods=['GET', 'POST'])
def edit_case_mange():
    form3 = EditApiCase()
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))

    if request.method == 'POST':
        name = form3.case_name.data
        case_id = int(form3.case_id.data)
        project_id = form3.project_id.data
        api_id = form3.api_id.data
        if APICase.query.filter_by(case_name=name).first() \
            and APICase.query.filter_by(case_name=name, api_id=api_id).first().id != case_id:
            flash(u'修改用例失败！存在多个相同名称。', 'danger')
        else:
            api_case = APICase.query.get_or_404(case_id)
            try:
                api_case.case_name = form3.case_name.data
                api_case.case_desc = form3.case_desc.data
                api_case.api_id = form3.api_id.data
                api_case.project_id = form3.project_id.data
                api_case.case_req = form3.case_req.data
                # api_case.case_head_add = form3.case_head_add.data
                api_case.expect_result = form3.expect_result.data
                api_case.Extract_failed = form3.Extract_failed.data
                api_case.case_status = form3.case_valid.data
                api_case.Operator_name = session["username"]
                db.session.add(api_case)
                db.session.commit()
                flash(u'修改用例信息成功！', 'success')
            except:
                flash(u'操作异常，请稍后重试', 'danger')

    return redirect(url_for('.apicase_mange', form3=form3, id=form3.api_id.data,project_id=form3.project_id.data))


@auth_option.route('/run/<string:evo_type>/<int:case_id>', methods=['GET', 'POST'])
def run_case_debug(case_id, evo_type):
    # case_ids = []
    if evo_type == 'None':
        config_env = [(m.project_id + '_' + m.config_name, m.config_name) for m in
                      ConfigParse.query.filter_by(project_id=(APICase.query.filter_by(id=case_id).first().project_id)).group_by(ConfigParse.project_id, ConfigParse.config_name)]

        evo_type = config_env[0][0]
    log_name = "_" + str(case_id) + "_" + str(datetime.datetime.now().strftime('%y%m%d%H%M%S')) + '.log'
    try:
        logs_info = []
        rc = RunCase(evo_type, log_name, 0, case_id)
        rc.run()
        logs_info = log_file(log_name, logs_info)
        return jsonify({"respcode": '000', 'desc': '用例执行完成！！', 'log_info': logs_info})
    except Exception as e:
        logs_info = log_file(log_name)
        logs_info.append(e)
        return jsonify({"respcode": '999', 'desc': '用例执行失败！！', 'log_info': logs_info})


@auth_option.route('/project/run_mange', methods=['GET', 'POST'])
def run_mange():
    project_id = request.args.get('project_id', -1, type=int)  # 项目ID
    form = RunMange(project_id=project_id)
    form2 = AddRunMange()
    form4 = EditRunMange()
    projects = Project.return_project()
    projects.append(('-1', u'全部'))
    form.project_id.choices = projects
    form2.project_id.choices = projects
    form4.project_id.choices = projects
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))

    run_manage_infos = RunCaseConfig.query.order_by(RunCaseConfig.id.desc()).all()

    if request.method == 'POST':
        if form.project_id.data == -1:
            run_manage_infos = RunCaseConfig.query.order_by(RunCaseConfig.id.desc()).all()
        else:
            run_manage_infos = RunCaseConfig.query.filter_by(project_id=form.project_id.data).all()
        if len(run_manage_infos) == 0:
            flash(u'根据项目名称:{0}未查出相关项目信息'.format(form.project_id.data), 'danger')
        else:
            return render_template("runmanage.html", form=form, form2=form2, form4=form4, len_run_manage=len(run_manage_infos), run_manage_infos=run_manage_infos, project=Project, api_id=0)

    return render_template("runmanage.html", form=form, form2=form2, form4=form4, len_run_manage=len(run_manage_infos), run_manage_infos=run_manage_infos, project=Project, api_id=0,run_id=0)

@auth_option.route('/add/run_mange', methods=['GET', 'POST'])
def add_run_mange():
    form2 = AddRunMange()
    if request.method == 'POST':
        run_config_option = RunCaseConfig.query.filter_by(plan_name=form2.plan_name.data, project_id=form2.project_id.data).first()
        if run_config_option:
            flash(u'添加运行配置失败！该项目下已经存在相同的运行配置。', 'danger')
        else:
            try:
                run_config_info = RunCaseConfig(project_id=form2.project_id.data, plan_name=form2.plan_name.data,
                                                run_mode=form2.run_mode.data,
                                                config_status=form2.config_status.data)
                db.session.add(run_config_info)
                db.session.commit()

                run_config_new = RunCaseConfig.query.filter_by(plan_name=form2.plan_name.data,
                                                                  project_id=form2.project_id.data).first()
                r_id = run_config_new.id
                func = 'APP:run_case'
                args = (run_config_new.id, run_config_new.project_id+'_'+'测试环境')
                trigger = 'cron'

                if '{' in run_config_new.cron_time and '}' in run_config_new.cron_time:
                    run_time = eval(run_config_new.cron_time)
                    day_of_week = run_time['day_of_week']
                    hour = run_time['hour']
                    minute = run_time['minute']
                    job = scheduler.add_job(func=func, id=r_id, args=args, trigger=trigger, hour=hour, day_of_week=day_of_week,
                                            minute=minute, replace_existing=True)
                    flash(u'添加运行配置成功！', 'success')
                else:
                    flash(u'cron 格式不正确,不能够进行设置定时任务', 'danger')

            except:
                flash(u'操作异常，请稍后重试', 'danger')
        return redirect(url_for('.run_mange', form2=form2))


@auth_option.route('/project/editconfig', methods=['GET', 'POST'])
def editconfig_mange():
    form4 = EditRunMange()
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))
    if request.method == 'POST':
        plan_name = form4.plan_name.data

        project_id = int(form4.project_id.data)
        if RunCaseConfig.query.filter_by(plan_name=plan_name).first() \
                and RunCaseConfig.query.filter_by(plan_name=plan_name).first().project_id != project_id:
            flash(u'修改配置失败！存在多个相同名称。', 'danger')
        else:
            config_info = RunCaseConfig.query.get_or_404(form4.run_id.data)

            try:
                config_info.plan_name = form4.plan_name.data
                config_info.config_status = form4.config_status.data
                config_info.cron_time = form4.run_time.data
                config_info.run_mode = form4.run_mode.data
                db.session.add(config_info)
                db.session.commit()

                r_id = str(config_info.id)
                func = 'APP:run_case'
                args = (config_info.id, str(config_info.project_id) + '_' + '测试环境')
                trigger = 'cron'
                if '{' in form4.run_time.data and '}' in form4.run_time.data:
                    run_time = eval(form4.run_time.data)
                    day_of_week = run_time['day_of_week']
                    hour = run_time['hour']
                    minute = run_time['minute']
                    job = scheduler.add_job(func=func, id=r_id, args=args, trigger=trigger, hour=hour,
                                            day_of_week=day_of_week,
                                            minute=minute, replace_existing=True)
                    flash(u'修改项目信息成功！', 'success')
                else:
                    flash(u'cron 格式不正确,不能够进行设置定时任务', 'danger')

            except:
                flash(u'操作异常，请稍后重试', 'danger')

    return redirect(url_for('.run_mange', form4=form4))

@auth_option.route('/pause/<string:job_id>')
def pausejob(job_id):
    # 暂停任务
    try:
        scheduler.pause_job(job_id)
        flash(u'删除任务成功！！', 'success')
    except:
        flash(u'不存在的任务！！', 'danger')
    return redirect(url_for('.run_mange'))

@auth_option.route('/resume/<string:job_id>')
def resumejob(job_id):
    # 恢复任务
    scheduler.resume_job(job_id)
    return redirect(url_for('.run_mange'))


@auth_option.route('/add/getconfigvalue/<int:id>', methods=['GET', 'POST'])
def get_config_by_id(id):
    config_value = RunCaseConfig.query.get_or_404(id)

    if request.is_xhr:
        return jsonify({
            'run_id': id,
            'plan_name': config_value.plan_name,
            'project_id': config_value.project_id,
            'case_id': config_value.sort_id,
            'run_time': config_value.cron_time,
            'run_mode': config_value.run_mode,
            'config_status': config_value.config_status
        })

@auth_option.route('/sortcase/<int:project_id>/<int:api_id>/<int:run_id>', methods=['GET', 'POST'])
def sort_case(project_id, api_id, run_id):
    form = SortCase()
    run_case_list = []
    case_ids = ''
    all_case_ids = []
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))

    #  获取项目下的所有 case_id
    cases_info = APICase.query.filter_by(project_id=project_id).all()

    if cases_info:
        for case_info in cases_info:
            all_case_ids.append(case_info.id)
    else:

        flash(u'根据项目名称:无测试用例', 'danger')
    # 查询配置运行模式 3 为用例，1,2 接口形式
    run_config_info = RunCaseConfig.query.filter_by(id=run_id).first()
    if run_config_info.run_mode != '3':  # 判断是否已经配置过，如果配置过加载 配置过API的
        config_info = CaseSort.query.filter_by(api_id=api_id, run_config_id=run_id).first()
        if config_info:
            if config_info.case_id:
                case_ids = config_info.case_id
                case_id_list = config_info.case_id.split(',')
                for case_id in case_id_list:
                    if case_id:
                        api_case = APICase.query.filter_by(id=case_id).first()
                        run_case_list.append(api_case)
                    else:
                        continue
            else:
                api_case_all = APICase.query.filter_by(api_id=api_id).all()
                run_case_list = api_case_all

        else:
            api_case_all = APICase.query.filter_by(api_id=api_id).all()
            run_case_list = api_case_all
    else:
        if run_config_info.sort_id:
            case_ids = run_config_info.sort_id
            for case_id in run_config_info.sort_id.split(','):
                if case_id:
                    api_case = APICase.query.filter_by(id=case_id).first()
                    run_case_list.append(api_case)
                    all_case_ids.remove(int(case_id))
            for case_id_other in all_case_ids:
                api_case = APICase.query.filter_by(id=case_id_other).first()
                run_case_list.append(api_case)

        else:
            api_case_all = APICase.query.filter_by(project_id=project_id).all()
            run_case_list = api_case_all
    if len(run_case_list) == 0:
        flash(u'根据项目名称:无测试用例', 'danger')

    return render_template('sortcase.html', apicases=run_case_list, len_apicases=len(run_case_list),
                           projectapi=ProjectAPI, project=Project, apicase=APICase, form=form, api_id=api_id,
                           run_id=run_id, run_mode=run_config_info.run_mode, cases_ids=case_ids)

# @auth_option.route('/sortcase/<int:projet_id><int:run_model>/<string:plan_name>', methods=['GET', 'POST'])
# def sort_api(plan_name, projet_id, run_model):
#     form = SortApi()
#     run_api_list = []
#     if 'username' not in session:
#         return redirect(url_for("auth_login.login"))
#     # 判断是否已经配置过，如果配置过加载 配置过的
#     config_info = RunCaseConfig.query.filter_by(plan_name=plan_name, project_id=projet_id, run_mode=run_model).first()
#     if config_info.sort_id:
#         api_id_list = config_info.sort_id.split(',')
#         for api_id in api_id_list:
#             if api_id:
#                 api_info = ProjectAPI.query.filter_by(id=api_id).first()
#                 run_api_list.append(api_info)
#             else:
#                 continue
#     else:
#         api_all = ProjectAPI.query.all()
#         run_api_list = api_all
#
#
#     if len(run_api_list) == 0:
#         flash(u'根据项目名称:无测试用例', 'danger')
#
#     return render_template('sortapi.html', apis=run_api_list, len_api=len(run_api_list),
#                            projectapi=ProjectAPI, project=Project, apicase=APICase, form=form, run_id=config_info.id)

@auth_option.route('/savecase', methods=['POST'])
def save_case():
    respon_json = {}
    # 查询是否保存过 api 用例数据
    case_sort = CaseSort.query.filter_by(api_id=request.form['api_id'].strip(), run_config_id=request.form['run_id'].strip()).first()
    if case_sort:
        try:
            case_sort.case_id = ','.join(eval(request.form['case_ids']))
            db.session.commit()
            respon_json['status'] = 'ok'
        except:
            respon_json['status'] = 'fail'
    else:
        if request.form['run_mode'].strip() != '3':
            try:
                api_case = CaseSort(run_config_id=request.form['run_id'].strip(), api_id=request.form['api_id'].strip(),
                                    case_id=','.join(eval(request.form['case_ids'])))
                db.session.add(api_case)
                db.session.commit()
                respon_json['status'] = 'ok'
            except:
                respon_json['status'] = 'fail'

        else:
            try:
                run_case_info = RunCaseConfig.query.filter_by(id=request.form['run_id'].strip()).first()
                run_case_info.sort_id = ','.join(eval(request.form['case_ids']))
                db.session.add(run_case_info)
                db.session.commit()
                respon_json['status'] = 'ok'
            except:
                respon_json['status'] = 'fail'
    return json.dumps(respon_json)

@auth_option.route('/savesortapi', methods=['POST'])
def save_api():
    respon_json = {}
    try:
        run_config_info = RunCaseConfig.query.filter_by(id=request.form['run_id'].strip()).first()
        run_config_info.sort_id = request.form['sort_ids']
        db.session.add(run_config_info)
        db.session.commit()
        respon_json['status'] = 'ok'
    except:
        respon_json['status'] = 'fail'

    return json.dumps(respon_json)

@auth_option.route('/run_api/<string:projet_id><int:run_model>/<string:plan_name>', methods=['GET', 'POST'])
def sort_api(plan_name, projet_id, run_model):
    # 作为添加使用
    form = AddRunApi()
    run_api_list = []
    apis_ids = ''
    api_ids_all = []
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))

    # 获取项目下的所有API接口

    apis_info = ProjectAPI.query.filter_by(project_id=projet_id).all()
    if apis_info:
        for api_info in apis_info:
            api_ids_all.append(api_info.id)
    else:
        flash(u'项目名称下无接口信息', 'danger')
    # 判断是否已经配置过，如果配置过加载 配置过的
    config_info = RunCaseConfig.query.filter_by(plan_name=plan_name, project_id=projet_id, run_mode=run_model).first()
    if config_info.sort_id:
        apis_ids = config_info.sort_id
        api_id_list = config_info.sort_id.split(',')
        for api_id in api_id_list:
            if api_id:
                api_info = ProjectAPI.query.filter_by(id=api_id).first()
                run_api_list.append(api_info)
                api_ids_all.remove(int(api_id))
            else:
                continue
        for api_id_other in api_ids_all:
            api_info = ProjectAPI.query.filter_by(id=api_id_other).first()
            run_api_list.append(api_info)
    else:
        api_all = ProjectAPI.query.filter_by(project_id=projet_id).all()
        run_api_list = api_all

    if len(run_api_list) == 0:
        flash(u'根据项目名称:无接口信息', 'danger')
    return render_template('sortapi.html', apis=run_api_list, len_api=len(run_api_list),
                           projectapi=ProjectAPI, project=Project, apicase=APICase, form=form, run_id=config_info.id, apis_ids=apis_ids)

@auth_option.route('/add_api', methods=['GET', 'POST'])
def add_run_api():
    respon_json={}
    try:
        run_config_info = RunCaseConfig.query.filter_by(id=request.form['run_id'].strip()).first()
        run_config_info.sort_id = ','.join(eval(request.form['api_ids']))
        db.session.add(run_config_info)
        db.session.commit()
        respon_json['status'] = 'ok'
    except:
        respon_json['status'] = 'fail'

    return json.dumps(respon_json)


@auth_option.route('/debugcase/<int:case_id>', methods=['GET', 'POST'])
def debug_case(case_id):
    setup_cases = []
    case_info = APICase.query.filter_by(id=case_id).first()  # 用例信息

    # 查询project 与 api
    # 主 host 数据  根据配置 (项目层 使用 配置, 接口层 从配置中加载，可以修改  修改与不修改都保存在 api)
    project_info = Project.query.filter_by(id=case_info.project_id).first()  # 项目信息

    api_info = ProjectAPI.query.filter_by(id=case_info.api_id).first()  # 接口信息

    # config_hosts = ConfigParse.query.filter_by(project_id=case_info.project_id, name='host').all()  # host 信息

    config_env = [(m.project_id+'_'+m.config_name, m.config_name) for m in ConfigParse.query.filter_by(project_id=case_info.project_id).group_by(ConfigParse.project_id, ConfigParse.config_name).all()]
    # config_heads = [(m.id, m.config_name) for m in ConfigParse.query.filter_by(project_id=case_info.project_id, name='head')]

    # config_heads = ConfigParse.query.filter_by(project_id=case_info.project_id, name='head').all()  # 头部信息

    case_setup_teardown_infos = StepTearDown.query.filter_by(the_belong='3', setup_teardown_id=case_id).all()  # 用例前置条件
    api_setup_teardown_infos = StepTearDown.query.filter_by(the_belong='2', setup_teardown_id=case_info.api_id).all()
    case_setup_info = ''
    case_teardown_info = ''
    if case_setup_teardown_infos:
        for setup_teardown_info in case_setup_teardown_infos:
            case_setup_info += setup_teardown_info.setup_pro+'|'
            case_teardown_info += setup_teardown_info.teardown_pro
            if setup_teardown_info.rely_id:
                case_setup_id = setup_teardown_info.rely_id
            else:
                case_setup_id = -1
    else:
        case_setup_id = -1
    api_setup_info = ''
    api_teardown_info = ''
    if api_setup_teardown_infos:
        for setup_teardown_info in api_setup_teardown_infos:
            api_setup_info += setup_teardown_info.setup_pro+"|"
            api_teardown_info += setup_teardown_info.teardown_pro+'|'
            if setup_teardown_info.rely_id:
                api_setup_id = setup_teardown_info.rely_id
            else:
                api_setup_id = -1
    else:
        api_setup_id = -1

    if case_setup_info == '':
        case_setup_info = '无'
    if api_setup_info == '':
        api_setup_info = '无'

    cases_ids = [(m.id, m.case_name) for m in APICase.query.filter_by(project_id=case_info.project_id)]

    cases_ids.append((-1, '无'))
    form = DebugCaseForm(api_url=api_info.api_url, api_relay_id=api_setup_id, case_relay_id=case_setup_id,
                         api_setup_step=api_setup_info, case_setup_step=case_setup_info,
                         api_method=api_info.api_method, case_head=api_info.api_heard, case_req=case_info.case_req,
                         expect_reslt=case_info.expect_result)
    form.host.choices = config_env
    # form.pro_head.choices = config_heads
    form.api_relay_id.choices = cases_ids
    form.case_relay_id.choices = cases_ids
    # form.setup_step.data = setup_cases
    if request.method == 'POST':
        try:
            case_info.case_req = form.case_req.data
            case_info.expect_result = form.expect_reslt.data
            db.session.add(case_info)
            db.session.commit()

            api_info.api_url = form.api_url.data
            api_info.api_method = form.api_method.data
            api_info.api_heard = form.case_head.data
            db.session.add(api_info)
            db.session.commit()
            flash(u'修改用例信息成功！', 'success')
        except:
            flash(u'操作异常，请稍后重试', 'danger')

    return render_template('casedebug.html', form=form, api_info=api_info, project_info=project_info, case_info=case_info)


@auth_option.route('/config/mange', methods=['GET', 'POST'])
def config_mange():
    form = ConfigMange()
    form2 = AddConfig()
    form3 = EditConfigForm()
    projects = Project.return_project()
    form2.project_id.choices = projects
    form3.project_id.choices = projects
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))

    config_paras = ConfigParse.query.order_by(ConfigParse.id.desc()).all()

    # if request.method == 'POST':
    #     projects = Project.query.filter_by(name=form.project_name.data).all()
    #     if len(projects) == 0:
    #         flash(u'根据项目名称:{0}未查出相关项目信息'.format(form.project_name.data), 'danger')
    #     else:
    #         return render_template("configparas.html", form=form, form2=form2, form3=form3, len_projects=len(projects), projects=projects)

    return render_template("configparas.html", form=form, form2=form2, form3=form3, len_config_paras=len(config_paras), config_paras=config_paras,project=Project)

@auth_option.route('/add/config', methods=['GET', 'POST'])
def add_config():
    form2 = AddConfig()
    if request.method == 'POST':
        project_option = ConfigParse.query.filter_by(config_name=form2.config_name.data, project_id=form2.project_id.data, name=form2.name.data).first()
        if project_option:
            flash(u'添加配置失败！该项目下存在相同名称配置。', 'danger')
        else:
            try:
                # url=form2.project_url.data,
                config_info = ConfigParse(name=form2.name.data,
                                      value=form2.value.data,
                                      project_id=form2.project_id.data,
                                      config_name=form2.config_name.data, Operator_name=session['username'])
                db.session.add(config_info)
                db.session.commit()
                flash(u'添加变量配置成功！', 'success')
            except:
                flash(u'操作异常，请稍后重试', 'danger')
        return redirect(url_for('.config_mange', form2=form2))

@auth_option.route('/config/editmange', methods=['GET', 'POST'])
def edit_config_mange():
    form3 = EditConfigForm()
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))
    if request.method == 'POST':
        config_name = form3.config_name.data
        config_id = int(form3.config_id.data)
        if ConfigParse.query.filter_by(config_name=config_name, project_id=form3.project_id.data, name=form3.name.data).first()\
                and ConfigParse.query.filter_by(config_name=config_name, project_id=form3.project_id.data, name=form3.name.data).first().id != config_id:
            flash(u'编辑配置失败！存在相同的配置名称！', 'danger')
        else:
            config_info = ConfigParse.query.get_or_404(config_id)
            try:
                config_info.name=form3.name.data
                config_info.value=form3.value.data
                config_info.config_name=form3.config_name.data
                config_info.project_id=form3.project_id.data
                config_info.Operator_name = session['username']
                db.session.add(config_info)
                db.session.commit()
                flash(u'修改配置信息成功！', 'success')
            except:
                flash(u'操作异常，请稍后重试', 'danger')

    return redirect(url_for('.config_mange', form3=form3))

@auth_option.route('/get/config/<int:id>', methods=['GET', 'POST'])
def get_config_parse_by_id(id):
    config_info = ConfigParse.query.get_or_404(id)
    if request.is_xhr:
        return jsonify({
            'config_id': str(id),
            'config_name': config_info.config_name,
            # 'project_url': project.url,
            'name': config_info.name,
            'value': config_info.value,
            'project_id':config_info.project_id
        })


@auth_option.route('/get/setup/<string:belong_id><string:id>/<string:project_id><string:api_id>', methods=['GET', 'POST'])
def get_setup_id(belong_id, id, project_id, api_id):
    # config_info = ConfigParse.query.get_or_404(id)
    rely_id_json = {'-1': '无'}
    case_infos = APICase.query.filter_by(project_id=project_id).all()
    for case_info in case_infos:
        rely_id_json[str(case_info.id)] = case_info.case_name
    if request.is_xhr:
        return jsonify({
            "setup_teardown_id": id,
            "belong_id": belong_id,
            'project_id': project_id,
            'api_id': api_id,
            'rely_id_json': rely_id_json
        })


@auth_option.route('/add/setup/', methods=['GET', 'POST'])
def add_setup():
    form5 = SetupTearDownForm()
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))
    if request.method == 'POST':
        try:
            setup_teardown_info = StepTearDown(setup_teardown_id=form5.setup_teardown_id.data,
                                      the_belong=form5.the_belong.data, rely_id=form5.relay_id.data,
                                      setup_pro=form5.setup_pro.data, teardown_pro=form5.teardown_pro.data)
            db.session.add(setup_teardown_info)
            db.session.commit()
            flash(u'添加前后置信息成功！', 'success')
        except Exception as e:
            flash(u'操作异常，请稍后重试 ,%s' % e, 'danger')
    return redirect(url_for('.project_mange', form5=form5))


@auth_option.route('/add/apisetup', methods=['GET', 'POST'])
def add_api_setup():
    form5 = SetupTearDownForm()
    print(id)
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))
    if request.method == 'POST':
        try:
            setup_teardown_info = StepTearDown(setup_teardown_id=form5.setup_teardown_id.data,
                                      the_belong=form5.the_belong.data, rely_id=form5.relay_id.data,
                                      setup_pro=form5.setup_pro.data, teardown_pro=form5.teardown_pro.data)
            db.session.add(setup_teardown_info)
            db.session.commit()
            flash(u'添加前后置信息成功！', 'success')
        except Exception as e:
            flash(u'操作异常，请稍后重试 ,%s' % e, 'danger')
    return redirect(url_for('.projectAPI_mange', form5=form5, id=form5.project_id.data))


@auth_option.route('/add/casesetup/', methods=['GET', 'POST'])
def add_case_setup():
    form5 = SetupTearDownForm()

    if 'username' not in session:
        return redirect(url_for("auth_login.login"))
    if request.method == 'POST':
        try:
            setup_teardown_info = StepTearDown(setup_teardown_id=form5.setup_teardown_id.data,
                                      the_belong=form5.the_belong.data, rely_id=form5.relay_id.data,
                                      setup_pro=form5.setup_pro.data, teardown_pro=form5.teardown_pro.data)
            db.session.add(setup_teardown_info)
            db.session.commit()
            flash(u'添加前后置信息成功！', 'success')
        except Exception as e:
            flash(u'操作异常，请稍后重试 ,%s' % e, 'danger')
    return redirect(url_for('.projectAPI_mange', form5=form5, id=form5.project_id.data))


@auth_option.route('/setupteardown/mange', methods=['GET', 'POST'])
def setupteardown_mange():
    form = SearchSetupTearDownForm()
    form2 = EditSetupTearDownForm()
    apicase = APICase.return_project()
    form2.relay_id.choices = apicase
    if 'username' not in session:
        return redirect(url_for("auth_login.login"))

    setup_teardown_infos = StepTearDown.query.order_by(StepTearDown.id.desc()).all()

    if request.method == 'POST':
        if form.name.data == '':
            setup_teardown_infos = StepTearDown.query.filter_by(the_belong=form.the_belong.data).all()
        else:
            setup_teardown_infos = []
            if form.the_belong.data == '1':
                project_infos = Project.query.filter(Project.name.like('%{0}%'.format(form.name.data))).all()
            elif form.the_belong.data == '2':
                project_infos = ProjectAPI.query.filter(ProjectAPI.api_name.ilike('%{0}%'.format(form.name.data))).all()
            else:
                project_infos = APICase.query.filter(APICase.case_name.ilike('%{0}%'.format(form.name.data))).all()

            if project_infos:
                for project_info in project_infos:
                    setup_teardown = StepTearDown.query.filter_by(the_belong=form.the_belong.data, setup_teardown_id=project_info.id).all()
                    for setup_teardown_info in setup_teardown:
                        setup_teardown_infos.append(setup_teardown_info)
            else:
                setup_teardown_infos = project_infos

        if len(setup_teardown_infos) == 0:
            flash(u'未查出前后置信息!!', 'danger')
            return render_template("setupteardownmanage.html", form=form, form2=form2, len_setup_teardown_infos=len(setup_teardown_infos), setup_teardown_infos=setup_teardown_infos,
                                   project=Project, projectapi=ProjectAPI, apicase=APICase)
        else:
            return render_template("setupteardownmanage.html", form=form, form2=form2, len_setup_teardown_infos=len(setup_teardown_infos), setup_teardown_infos=setup_teardown_infos,
                                   project=Project, projectapi=ProjectAPI, apicase=APICase)
    return render_template("setupteardownmanage.html", form=form, form2=form2, len_setup_teardown_infos=len(setup_teardown_infos),
                           setup_teardown_infos=setup_teardown_infos, project=Project, projectapi=ProjectAPI, apicase=APICase)


@auth_option.route('/get/setup_info/<int:id>', methods=['GET', 'POST'])
def get_setup_info(id):
    setup_tear_down = StepTearDown.query.get_or_404(id)
    rely_id_json = {'-1': '无'}
    if setup_tear_down.the_belong == '1':
        project_id = setup_tear_down.setup_teardown_id
    elif setup_tear_down.the_belong == '2':
        api_id = setup_tear_down.setup_teardown_id
        api_infos = ProjectAPI.query.filter_by(id=api_id).first()
        project_id = api_infos.project_id
    else:
        case_id = setup_tear_down.setup_teardown_id
        case_infos = APICase.query.filter_by(id=case_id).first()
        project_id = case_infos.project_id
    case_infos = APICase.query.filter_by(project_id=project_id).all()
    for case_info in case_infos:
        rely_id_json[str(case_info.id)] = case_info.case_name
    if request.is_xhr:
        return jsonify({
            'id':setup_tear_down.id,
            "setup_teardown_id": setup_tear_down.setup_teardown_id,
            "belong_id": setup_tear_down.the_belong,
            'rely_id': setup_tear_down.rely_id,
            'setup_pro': setup_tear_down.setup_pro,
            'teardown_pro': setup_tear_down.teardown_pro,
            'rely_id_json':rely_id_json
        })

@auth_option.route('/setup/editmange', methods=['GET', 'POST'])
def editsetup_info():
    form2 = EditSetupTearDownForm()

    if 'username' not in session:
        return redirect(url_for("auth_login.login"))

    if request.method == 'POST':
        the_belong = form2.the_belong.data
        setup_teardown_id = form2.setup_teardown_id.data
        setup_id = int(form2.SetupTearDown_id.data)
        if StepTearDown.query.filter_by(the_belong=the_belong, setup_teardown_id=setup_teardown_id).first() \
            and Project.query.filter_by(the_belong=the_belong, setup_teardown_id=setup_teardown_id).first().id != setup_id:
            flash(u'修改失败。', 'danger')
        else:
            setup_teardown = StepTearDown.query.get_or_404(setup_id)
            try:

                setup_teardown.setup_pro = form2.setup_pro.data
                setup_teardown.teardown_pro = form2.teardown_pro.data
                setup_teardown.rely_id = form2.relay_id.data
                db.session.add(setup_teardown)
                db.session.commit()
                flash(u'修改前后置信息成功！', 'success')
            except:
                flash(u'操作异常，请稍后重试', 'danger')

    return redirect(url_for('.setupteardown_mange', form2=form2))