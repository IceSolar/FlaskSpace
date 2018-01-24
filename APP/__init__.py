# coding: utf-8
__author__ = 'wuyan'
from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.moment import Moment
from flask_moment import Moment
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from config import *
from celery import Celery
from flask_apscheduler import APScheduler
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config["SECRET_KEY"] = SECRET_KEY
app.config["ARTICLES_PER_PAGE"] = ARTICLES_PER_PAGE
app.config["COMMENTS_PER_PAGE"] = COMMENTS_PER_PAGE
app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = CELERY_RESULT_BACKEND
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
scheduler = APScheduler()
db = SQLAlchemy(app)
moment = Moment() #依赖moment.js和jquery.js 日期处理类库

# def listen_aps():
#     from .RunCase.common.mydb import MyDb
#     import datetime
#     db_conn = MyDb(db_path, 'sqlite')
#     apscheduler_sql = 'select env__name, apscheduler_name,day_of_week,hour,minute from apscheduler'
#     apscheduler_infos = db_conn.select_many_record(apscheduler_sql)
#     jobs = []
#     for apscheduler_info in apscheduler_infos:
#         log_name = apscheduler_info[1].split('_')[1] + str(datetime.datetime.now().strftime('%y%m%d%H%M%S')) + '.log'
#         job_one = {}
#         job_one['id'] = apscheduler_info[1]
#         job_one['func'] = 'APP:run_case'
#         job_one['trigger'] = 'cron'
#         job_one['day_of_week'] = apscheduler_info[2]
#         job_one['hour'] = apscheduler_info[3]
#         job_one['minute'] = apscheduler_info[4]
#         job_one['args'] = (apscheduler_info[0], log_name, apscheduler_info[1].split('_')[1])
#         jobs.append(job_one)
#     return jobs
#
# class Config(object):
#
#     # rc = RunCase('1_测试环境', log_name, 2)
#     JOBS = listen_aps()
#     basedir = os.path.abspath(os.path.dirname(__file__))
#
#     if os.path.lexists(os.path.join(basedir, 'jobs.sqlite')):
#
#         os.remove(os.path.join(basedir, 'jobs.sqlite'))
#
#     SCHEDULER_JOBSTORES = {
#         'default': SQLAlchemyJobStore(url='sqlite:///' + os.path.join(basedir, 'jobs.sqlite'))
#     }
#
#     SCHEDULER_EXECUTORS = {
#         'default': {'type': 'threadpool', 'max_workers': 20}
#     }
#
#     SCHEDULER_JOB_DEFAULTS = {
#         'coalesce': False,
#         'max_instances': 3
#     }
#
#     SCHEDULER_API_ENABLED = True
# #
def run_case(run_id, env):
    from .RunCase.runcase import RunCase
    import datetime
    log_name = str(run_id) + '_' + str(datetime.datetime.now().strftime('%y%m%d%H%M%S')) + '.log'
    rc = RunCase(env, log_name, run_id)
    rc.run()
# def job1(a, b):
#     print(str(a) + ' ' + str(b))
class Config(object):
    JOBS = []
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///' + os.path.join(basedir, 'jobs.sqlite'))
    }
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }
    SCHEDULER_API_ENABLED = True


def create_app():
    # CsrfProtect(app) #表单令牌 表单保护你免受 CSRF 威胁，你不需要有任何担心
    moment.init_app(app)

    from .auth_login import auth_login as auth_blueprint
    from .report import casereport as main_blueprint
    from .auth import auth_option as admin_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint, url_prefix='/report')
    app.register_blueprint(admin_blueprint, url_prefix='/auth_option')
    # from .job import job_value as job
    # app.register_blueprint(job, url_prefix='/job')
    celery.conf.update(app.config)
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    return app