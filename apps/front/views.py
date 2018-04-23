#encoding: utf-8
from flask import (
    Blueprint,
    views,
    render_template,
    request
)
from .forms import SingupForm
from utils import restful,safeutils
from .models import FrontUser
from exts import db

bp = Blueprint("front",__name__)

@bp.route('/')
def index():
    return "front index"


class SingupView(views.MethodView):
    def get(self):
        return_to = request.referrer #获取上个页面
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_singup.html',return_to=return_to)
        else:
            return render_template('front/front_singup.html')

    def post(self):
        form = SingupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())
            return restful.parms_error(message=form.get_error())


bp.add_url_rule('/singup/',view_func=SingupView.as_view('signup'))