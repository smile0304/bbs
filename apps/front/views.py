#encoding: utf-8
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    url_for
)
from .forms import SingupForm,SinginForm,AddPostForm
from utils import restful,safeutils
from .models import FrontUser
from exts import db
from ..models import BannerModel,BoardModel,PostModel
from .decorators import login_required
import config

bp = Blueprint("front",__name__)

@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    context = {
        'banners' : banners,
        'boards': boards
    }
    return render_template("front/front_index.html",**context)


@bp.route('/apost/',methods=['GET','POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template("front/front_apost.html",boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.parms_error(message="没有这个板块!")
            post = PostModel(title=title,content=content)
            post.board = board
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.parms_error(message=form.get_error())

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


class SinginView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != \
            url_for('front.singup') and safeutils.is_safe_url(return_to):
            return render_template("front/front_signin.html",return_to=return_to)
        return render_template("front/front_signin.html")

    def post(self):
        form = SinginForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remeber.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.parms_error(message="手机号或密码错误")
        else:
            return restful.parms_error(message=form.get_error())


bp.add_url_rule('/singup/',view_func=SingupView.as_view('singup'))
bp.add_url_rule('/singin/',view_func=SinginView.as_view('singin'))