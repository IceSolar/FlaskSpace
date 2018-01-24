# coding: utf-8

# from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import SelectField, StringField, TextAreaField, SubmitField, PasswordField, RadioField, IntegerField, Label
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class AddProject(Form):
    project_name = StringField(u'项目名', validators=[DataRequired()])
    # project_url = StringField(u'项目URL', validators=[DataRequired()])
    project_remark = TextAreaField(u'备注信息', validators=[DataRequired()])
    is_valid = RadioField(u'项目属性', choices=[('true', u'有效'), ('flase', u'失效')], default='true')


class EditProjectForm(AddProject):
    project_id = StringField(validators=[DataRequired()])


class ProjectMange(Form):
    project_name = StringField(validators=[DataRequired()])


class ProjectAPIMag(Form):
    api_name = StringField(u'接口名', validators=[DataRequired()])
    project_id = SelectField(u'所属项目', coerce=int, validators=[DataRequired()])


class addProjectAPI(ProjectAPIMag):
    project_name = StringField(u'项目名', validators=[DataRequired()])
    project_id = SelectField(u'所属项目', coerce=int, validators=[DataRequired()])
    api_url = StringField(u'接口url', validators=[DataRequired()])

    api_heard = TextAreaField(u'接口头', validators=[DataRequired()])

    api_resp = TextAreaField(u'接口返回模板', validators=[DataRequired()])

    api_req = TextAreaField(u'接口请求模板', validators=[DataRequired()])

    api_method = RadioField(u'接口属性', choices=[ ('POST', u'POST'), ('GET', u'GET')], default='POST')

    api_valid = RadioField(u'接口属性', choices=[('true', u'有效'), ('flase', u'失效')], default='true')


class EditAPIForm(addProjectAPI):
    api_id = StringField(validators=[DataRequired()])


class ApiCaseMange(Form):
    case_name = StringField(u'用例名称', validators=[DataRequired()])
    project_id = SelectField(u'所属项目', coerce=int, validators=[DataRequired()])
    api_id = SelectField(u'所属接口', coerce=int, validators=[DataRequired()])


class addApiCase(ApiCaseMange):

    # rely_case_id = SelectField(u'前置条件', coerce=int, validators=[DataRequired()])

    case_desc = TextAreaField(u'用例描述', validators=[DataRequired()])

    case_req = TextAreaField(u'用例参数', validators=[DataRequired()])

    # case_head_add = TextAreaField(u'用例头', validators=[DataRequired()])

    expect_result = TextAreaField(u'期望结果', validators=[DataRequired()])

    Extract_failed = TextAreaField(u'提取返回结果', validators=[DataRequired()])

    case_valid = RadioField(u'接口属性', choices=[('true', u'有效'), ('flase', u'失效')], default='true')


class EditApiCase(addApiCase):
    case_id = StringField(validators=[DataRequired()])


class RunMange(Form):
    project_id = SelectField(u'所属项目', coerce=int, validators=[DataRequired()])
    # api_id = SelectField(u'所属接口', coerce=int, validators=[DataRequired()])


class AddRunMange(RunMange):
    plan_name = StringField(u'套件名', validators=[DataRequired()])
    sort_id = TextAreaField(u'运行Case', validators=[DataRequired()])
    config_status = RadioField(u'套件属性', choices=[('true', u'有效'), ('flase', u'失效')], default='true')
    run_mode = RadioField(u'运行方式', choices=[('2', u'接口套件'), ('3', u'用例套件')], default='1')
    # run_mode = RadioField(u'运行方式', choices=[('1', u'全部运行'), ('2', u'套件运行')], default='1')
    run_time = TextAreaField(u'运行时间cron', validators=[DataRequired()])


class EditRunMange(AddRunMange):
    run_id = StringField(validators=[DataRequired()])


class SortApi(Form):
    api_ids = StringField(validators=[DataRequired()])


class SortCase(Form):
    # run_case_id = StringField(validators=[DataRequired()])
    case_ids = StringField(validators=[DataRequired()])


class AddRunApi(Form):
    api_ids = StringField(validators=[DataRequired()])


class DebugCaseForm(Form):

    # host = StringField(u'HOST', validators=[DataRequired()])

    host = SelectField(u'项目', validators=[DataRequired()])

    pro_head = SelectField(u'公共头域', validators=[DataRequired()])

    api_setup_step = StringField(u'接口前置条件', validators=[DataRequired()])

    api_relay_id = SelectField(u'接口-前置用例', validators=[DataRequired()])

    case_setup_step = StringField(u'用例前置条件', validators=[DataRequired()])

    case_relay_id = SelectField(u'用例-前置用例', validators=[DataRequired()])

    # SelectField(u'前置条件', coerce=int, validators=[DataRequired()])

    api_url = StringField(u'接口url', validators=[DataRequired()])

    # api_method = RadioField(u'接口属性', choices=[('POST', u'POST'), ('GET', u'GET')], default='POST')

    api_method = SelectField(u'接口方法', choices=[('POST', 'POST'), ('GET', 'GET')])

    case_head = TextAreaField(u'接口头', validators=[DataRequired()])

    case_req = TextAreaField(u'请求参数', validators=[DataRequired()])

    expect_reslt = TextAreaField(u'期望结果', validators=[DataRequired()])

    teardown_step = TextAreaField(u'后置条件', validators=[DataRequired()])


class ConfigMange(Form):
    config_name = SelectField(u'所属环境', choices=[('测试环境', '测试环境'), ('生产环境', '生产环境')])
    name = SelectField(u'配置名', choices=[('db', 'db'), ('host', 'host'), ('head', 'head')])
    value = TextAreaField(u'参数值', validators=[DataRequired()])
    is_valid = RadioField(u'参数属性', choices=[('true', u'有效'), ('flase', u'失效')], default='true')


class AddConfig(ConfigMange):
    project_id = SelectField(u'所属项目', coerce=int, validators=[DataRequired()])


class EditConfigForm(ConfigMange):
    project_id = SelectField(u'所属项目', coerce=int, validators=[DataRequired()])
    config_id = StringField(validators=[DataRequired()])


class SetupTearDownForm(Form):
    setup_teardown_id = StringField(validators=[DataRequired()])
    the_belong = StringField(validators=[DataRequired()])
    # setup_type = SelectField(u'前置类型', choices=[('JSON', u'JSON'), ('SQL', u'SQL')], default='JSON')
    relay_id = SelectField(u'前置用例ID', validators=[DataRequired()])  # 只有当 为json 才可以选择
    setup_pro = TextAreaField(u'前置条件', validators=[DataRequired()])
    teardown_pro = TextAreaField(u'后置条件', validators=[DataRequired()])
    project_id = StringField(validators=[DataRequired()])
    api_id = StringField(validators=[DataRequired()])


class SearchSetupTearDownForm(Form):
    the_belong = SelectField(validators=[DataRequired()], choices=[('1', '项目'), ('2', '接口'), ('3', '用例')], default='1')
    name = StringField(validators=[DataRequired()])


class EditSetupTearDownForm(SetupTearDownForm):
    SetupTearDown_id = StringField(validators=[DataRequired()])
