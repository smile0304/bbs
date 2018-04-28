#encoding: utf-8

from ..forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp,EqualTo,ValidationError,InputRequired
from utils import ttcache

class SingupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[34578]\d{9}",message="请输入正确的手机号")])
    sms_captcha = StringField(validators=[Regexp(r"\w{4}",message="请输入正确的短信验证码")])
    username = StringField(validators=[Regexp(r".{4,20}",message="请输入正确格式的用户名")])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}",message="请输入正确格式的密码")])
    password2 = StringField(validators=[EqualTo("password1",message="两次输入的密码不同")])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}",message="请输入正确的图形验证码")])

    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_mem = ttcache.get(telephone)
        if not sms_captcha_mem and sms_captcha_mem.lower() != sms_captcha.lower():
            raise ValidationError(message="短信验证码错误!")

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        graph_captcha_mem = ttcache.get(graph_captcha)

        if not graph_captcha_mem:
            raise ValidationError(message="图形验证码错误!")

class SinginForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[34578]\d{9}", message="请输入正确的手机号")])
    password = StringField(validators=[EqualTo("password", message="两次输入的密码不同")])
    remeber = StringField()

class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message="请输入标题!")])
    content = StringField(validators=[InputRequired(message="请输入内容")])
    board_id = IntegerField(validators=[InputRequired(message="请输入板块ID")])

class AddComment(BaseForm):
    content = StringField(validators=[InputRequired(message="请输入评论内容")])
    post_id = IntegerField(validators=[InputRequired(message="请输入帖子ID")])
