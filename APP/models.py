# coding: utf-8
from APP import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
class User(db.Model):
    __tablename__ ='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120))
    # role = db.Column(db.SmallInteger, default = ROLE_USER)
    password_hash = db.Column(db.String(128))
    @staticmethod
    def insert_user(username,email,password):
        user = User(username=username, email= email, password=password)
        db.session.add(user)
        db.session.commit()
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False)
    # url = db.Column(db.String(200), unique=False)
    desc = db.Column(db.String(500), unique=False)
    Operator_name = db.Column(db.String(200), unique=False) #操作人
    project_status = db.Column(db.String(10), default=0, nullable=False)


    @staticmethod
    def return_project():
        project = [(m.id, m.name) for m in Project.query.all()]
        return project
class ProjectAPI(db.Model):
    __tablename__ = "projectapis"
    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(200), unique=False)
    api_url = db.Column(db.String(200), unique=False)
    api_desc = db.Column(db.String(500), unique=False)
    api_heard = db.Column(db.String(1000), unique=False)
    api_resp = db.Column(db.String(5000), unique=False)
    api_req = db.Column(db.String(5000), unique=False)
    api_method = db.Column(db.String(5000), unique=False)
    Operator_name = db.Column(db.String(200), unique=False) #操作人
    api_status = db.Column(db.String(10), nullable=False)
    project_id = db.Column(db.Integer, unique=False)

    @staticmethod
    def return_project():
        projectapi = [(m.id, m.api_name) for m in ProjectAPI.query.all()]
        return projectapi

class APICase(db.Model):
    __tablename__ = "apicase"
    id = db.Column(db.Integer, primary_key=True)
    case_name = db.Column(db.String(200), unique=False)
    case_desc = db.Column(db.String(500), unique=False)
    # rely_case_id = db.Column(db.Integer, unique=False)
    api_id = db.Column(db.Integer, unique=False)
    project_id = db.Column(db.Integer, unique=False)
    case_req = db.Column(db.String(1000), unique=False)
    # case_head_add = db.Column(db.String(1000), unique=False)
    expect_result = db.Column(db.String(1000), unique=False)
    Extract_failed = db.Column(db.String(1000), unique=False)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    Operator_name = db.Column(db.String(200), unique=False)  # 操作人
    case_status = db.Column(db.String(10), nullable=False)

    @staticmethod
    def return_project():
        apicase = [(m.id, m.case_name) for m in APICase.query.all()]
        return apicase


class RunCaseConfig(db.Model):
    __tablename__ = "runcaseconfig"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    plan_name = db.Column(db.String(500), unique=False)
    sort_id = db.Column(db.String(500), unique=False)
    run_mode = db.Column(db.String(5), unique=False)
    config_status = db.Column(db.String(10), unique=False)
    # 运行时间 定时任务也在此 配置 但是非必填项
    cron_time = db.Column(db.String(50), unique=False)
class CaseSort(db.Model):
    __tablename__ = "casesortconfig"
    id = db.Column(db.Integer, primary_key=True)
    run_config_id = db.Column(db.Integer, nullable=False)
    api_id = db.Column(db.String(50), unique=False)
    case_id = db.Column(db.String(500), unique=False)

class CaseResult(db.Model):
    __tablename__ = "caseresult"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    api_id = db.Column(db.Integer, nullable=False)
    case_id = db.Column(db.Integer, nullable=False)
    project_name = db.Column(db.String(100), unique=False)
    api_name = db.Column(db.String(100), unique=False)
    case_name = db.Column(db.String(100), unique=False)
    method = db.Column(db.String(10), unique=False)
    head = db.Column(db.String(1000), unique=False)
    params = db.Column(db.String(1000), unique=False)
    respon = db.Column(db.String(1000), unique=False)
    expect_result = db.Column(db.String(1000), unique=False)
    run_result = db.Column(db.String(10), unique=False)  # pass fail error
    result_reason = db.Column(db.String(500), unique=False)
    # plan_name = db.Column(db.String(100), unique=False)
    # run_mode = db.Column(db.String(100), unique=False)
    run_time = db.Column(db.Float, unique=False)
    run_id = db.Column(db.String(20), unique=False)
    run_batch = db.Column(db.Integer, unique=False)
    request_url = db.Column(db.String(100), unique=False)

class ConfigParse(db.Model):
    __tablename__ = "configparse"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    value = db.Column(db.String(500), unique=False)
    Operator_name = db.Column(db.String(200), unique=False)  # 操作人
    project_id = db.Column(db.String(50), unique=False)
    config_name = db.Column(db.String(50), unique=False)

class StepTearDown(db.Model):
    __tablename__ = "setupteardown"
    id = db.Column(db.Integer, primary_key=True)
    setup_teardown_id = db.Column(db.String(100), unique=False)  # 设置 project_id api_id case_id
    the_belong = db.Column(db.String(10), unique=False)  # 1项目 2接口 3用例
    rely_id = db.Column(db.String(10), unique=False)  # 关联ID 只有当 type 为 json
    setup_pro = db.Column(db.String(200), unique=False)
    teardown_pro = db.Column(db.String(200), unique=False)
    setup_type = db.Column(db.String(10), unique=False)  # sql json

class MiddelResult(db.Model):
    __tablename__ = "extract"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.String(100), unique=False)

    extract_field = db.Column(db.String(100), unique=False)

    extract_value = db.Column(db.String(100), unique=False)

class APSCheduler(db.Model):
    __tablename__ = "apscheduler"

    id = db.Column(db.Integer, primary_key=True)

    env__name = db.Column(db.String(100), unique=False)

    apscheduler_name = db.Column(db.String(100), unique=False)

    day_of_week = db.Column(db.String(100), unique=False)  # 0-6

    hour = db.Column(db.String(100), unique=False)  # 0-23

    minute = db.Column(db.String(100), unique=False)  # 0-59





