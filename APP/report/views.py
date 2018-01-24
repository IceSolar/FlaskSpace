# coding: utf-8
from . import casereport
from ..models import Project, CaseResult, ProjectAPI, APICase
from ..RunCase.common.mydb import MyDb
from flask import *
from config import *
__author__ = 'rudolf'
@casereport.route('/')
def report():
    # 获取项目数
    project_infos = Project().return_project()
    db_conn = MyDb(db_path, 'sqlite')  # 用例库
    max_run_batch_sql = " select max(run_batch) from caseresult "
    max_run_batch_ = db_conn.select_one_record(max_run_batch_sql)

    result_info_sql = "select run_result,count(1)  from caseresult where run_batch='{0}' GROUP BY run_result".format(max_run_batch_[0])
    result_infos = db_conn.select_many_record(result_info_sql)
    #, project_infos = project_infos
    fail = 0
    success = 0
    other = 0
    for result_info in result_infos:
        if result_info[0] == 'fail':
            fail = result_info[1]
        elif result_info[0] == 'success':
            success = result_info[1]
        else:
            other = + other
    page = request.args.get('page', 1, type=int)
    pagination = CaseResult.query.filter_by(run_batch=max_run_batch_[0]).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    case_results = pagination.items

    return render_template('casereport.html', project_infos=project_infos, projectapi=ProjectAPI, fail=fail, success=success,project_name=None,
                           other=other, case_results=case_results, pagination=pagination, endpoint='.report', page=page, json=json)

@casereport.route('/<int:project_id>')
def report_info(project_id):
    # 获取项目数
    project_infos = Project().return_project()
    db_conn = MyDb(db_path, 'sqlite')
    max_run_batch_sql = " select max(run_batch) from caseresult where project_id ='{0}'".format(project_id)
    max_run_batch_ = db_conn.select_one_record(max_run_batch_sql)
    result_info_sql = "select run_result,count(1)  from caseresult where run_batch='{0}' and  project_id ='{1}' GROUP BY run_result".format(max_run_batch_[0],str(project_id))
    result_infos = db_conn.select_many_record(result_info_sql)
    fail = 0
    success = 0
    other = 0
    for result_info in result_infos:
        if result_info[0] == 'fail':
            fail = result_info[1]
        elif result_info[0] == 'success':
            success = result_info[1]
        else:
            other = + other

    page = request.args.get('page', 1, type=int)
    pagination = CaseResult.query.filter_by(run_batch=max_run_batch_[0], project_id=str(project_id)).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)

    case_results = pagination.items

    return render_template('casereport.html', project_infos=project_infos, projectapi=ProjectAPI, fail=fail, project_name=Project.query.filter_by(id=project_id).first().name,
                           success=success, other=other, case_results=case_results, pagination=pagination,
                            endpoint='.report_info', page=page,
                           project_id=project_id, json=json)
