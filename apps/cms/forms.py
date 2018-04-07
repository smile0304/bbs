#encoding: utf-8

from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length

class LoginForm(Form):
    email = StringField(validators=[Email(message="邮箱格式不正确"),InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(5,20,message="请输入正确格式的密码")])
    remember = IntegerField()