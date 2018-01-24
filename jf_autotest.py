# coding: utf-8
from APP import create_app, db
from APP.models import User
db.create_all()
# User.insert_user(username=u'管理员', email='admin', password='123456')
app = create_app()

if __name__ == '__main__':
    # '192.168.23.115              192.168.20.243'
    app.run()
    # app.run(debug=True)
