__author__ = 'rudolf_han'

from flask import Blueprint

job_value = Blueprint("job", __name__)

from . import views
