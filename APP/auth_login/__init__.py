# coding: utf-8
__author__ = 'rudolf'
from flask import Blueprint

auth_login = Blueprint('auth_login', __name__)

from . import views

