# coding: utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'QADB.sqlite')
log_path = os.path.join(basedir, 'log')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'QADB.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
SECRET_KEY = 'secret key to protect from csrf'
WTF_CSRF_SECRET_KEY = 'random key for form'
CSRF_ENABLED = True
ARTICLES_PER_PAGE = 10
COMMENTS_PER_PAGE = 10
