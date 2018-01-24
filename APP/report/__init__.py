# coding: utf-8

from flask import Blueprint

casereport = Blueprint("report", __name__)

from . import views
