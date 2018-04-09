#encoding: utf-8

from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BaseForm

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式不正确"),InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(5,20,message="请输入正确格式的密码")])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(5, 20, message="请输入正确格式的旧密码")])
    newpwd = StringField(validators=[Length(5,20,message="请输入正确格式的新密码")])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message="两次密码不相等")])

