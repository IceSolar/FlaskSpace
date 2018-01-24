# coding: utf-8

from flask import Blueprint

auth_option = Blueprint("auth_option", __name__)

from . import views


