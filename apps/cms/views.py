#encoding: utf-8
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify,
)

from .forms import LoginForm,ResetpwdForm,ResetEmailForm
from .models import CMSUser,CMSPersmisson
from .decorators import login_required,permission_required
import config
from exts import db,mail
from flask_mail import Message
from utils import restful,ttcache
import string
import random
bp = Blueprint("cms",__name__,url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    session["login_info"] = "注销成功"
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template("cms/cms_profile.html")


class LoginViwe(views.MethodView):
    def get(self,message=None):
        if session.get("login_info"):
            message = session["login_info"]
            del session["login_info"]
            return render_template("cms/cms_login.html", message=message)
        return render_template("cms/cms_login.html", message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    #如果设置session.permanent，过期时间为31天
                    session.permanent = True
                return redirect(request.args.get("next") or url_for('cms.index'))
            else:
                return self.get(message="邮箱或密码错误")
        else:
            message = form.get_error()
            return self.get(message=message)


class RestPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.parms_error("旧密码错误!")
        else:
           return restful.parms_error(form.get_error())

class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetmail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.parms_error(form.get_error())

@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.post('email')
    if not email:
        return restful.parms_error("请传递邮箱")
    #给这个邮箱发送邮件
    source = list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(0,10)))
    captcha = "".join(random.sample(source,6))
    message = Message("bbs邮箱验证",recipients=['smile@smilehacker.net'],body="您的验证码是:%s" % captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    ttcache.set(email,captcha)
    return restful.success()


@bp.route('/posts/')
@login_required
@permission_required(CMSPersmisson.POSTER)
def posts():
    return render_template('cms/cms_posts.html')


@bp.route('/comments/')
@login_required
@permission_required(CMSPersmisson.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPersmisson.BORDER)
def boards():
    return render_template('cms/cms_boards.html')


@bp.route('/fusers/')
@login_required
@permission_required(CMSPersmisson.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@login_required
@permission_required(CMSPersmisson.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required
@permission_required(CMSPersmisson.All_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')
"""
测试邮箱发送功能
@bp.route('/email/')
def send_email():
    message = Message('bbs测试邮件',recipients=['smile@smilehacker.net'],body='test')
    mail.send(message)
    return "success!"
"""
bp.add_url_rule('/login/',view_func=LoginViwe.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=RestPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))
