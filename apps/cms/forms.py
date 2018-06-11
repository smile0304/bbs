#encoding: utf-8

from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo,ValidationError
from ..forms import BaseForm
from utils import ttcache
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式不正确"),InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(5,20,message="请输入正确格式的密码")])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(5, 20, message="请输入正确格式的旧密码")])
    newpwd = StringField(validators=[Length(5,20,message="请输入正确格式的新密码")])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message="两次密码不相等")])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱!")])
    captcha = StringField(validators=[Length(min=6,max=6,message="请输入正确的验证码")])

    def validate_captcha(self,filed):
        captcha = filed.data
        email = self.email.data
        captcha_cache = ttcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError("验证码错误！")

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("请使用不同的邮箱")

class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入轮播图名称")])
    image_url = StringField(validators=[InputRequired(message="请输入轮播图地址")])
    link_url = StringField(validators=[InputRequired(message="请输入轮播图跳转地址")])
    priority = IntegerField(validators=[InputRequired(message="请输入轮播图优先级")])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message="请输入轮播图的id")])

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入板块名称")])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message="请输入板块ID!")])