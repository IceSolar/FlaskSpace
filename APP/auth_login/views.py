# coding: utf-8
from . import auth_login
from ..models import User
from flask import *

__author__ = 'rudolf'

@auth_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['Username']).first()
        if user is not None and user.verify_password(request.form['Password']):
            session['username'] = user.username
            return redirect(url_for("auth_option.index"))
            #return 'hello word %s'% user.username
        else:
            flash(u'用户名密码错误请重试！', 'danger')
    return render_template('/login.html')
@auth_login.route('/logout')
def logout():
    session.pop("username")
    # flash(u'您已退出登陆。', 'success')
    return redirect(url_for("auth_login.login"))


