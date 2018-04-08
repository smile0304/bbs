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

from .forms import LoginForm,ResetpwdForm
from .models import CMSUser
from .decorators import login_required
import config
from exts import db
from utils import restful
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


bp.add_url_rule('/login/',view_func=LoginViwe.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=RestPwdView.as_view('resetpwd'))
