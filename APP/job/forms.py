from flask.ext.wtf import Form
from wtforms import SelectField, StringField, TextAreaField, SubmitField, PasswordField, RadioField, IntegerField, Label
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
__author__ = 'rudolf_han'
class JobMange(Form):
    project_id = SelectField(u'所属项目', coerce=int, validators=[DataRequired()])
    # api_id = SelectField(u'所属接口', coerce=int, validators=[DataRequired()])

class AddJobMange(JobMange):
    job_name = StringField(u'任务名', validators=[DataRequired()])
    run_time = StringField(u'运行时间cron', validators=[DataRequired()])

class EditRunMange(AddJobMange):
    run_id = StringField(validators=[DataRequired()])