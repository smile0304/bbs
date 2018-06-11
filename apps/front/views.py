#encoding: utf-8
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    url_for,
    g,
    abort
)
from .forms import SingupForm,SinginForm,AddPostForm,AddComment
from utils import restful,safeutils
from .models import FrontUser
from exts import db
from ..models import BannerModel,BoardModel,PostModel,CommentModel,HighlightModel
from .decorators import login_required
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy.sql import func
import config

bp = Blueprint("front",__name__)

@bp.route('/')
def index():
    board_id = request.args.get('bd',type=int,default=None)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    sort = request.args.get('st',type=int,default=1)
    boards = BoardModel.query.all()
    #posts = PostModel.query.all()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1) *config.PER_PAGE
    total = 0
    end = start + config.PER_PAGE
    query = None
    if sort==1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort==2:
        #加精的时间倒序
        query_obj = db.session.query(PostModel).outerjoin(HighlightModel).order_by(HighlightModel.create_time.desc(),PostModel.create_time.desc())
    elif sort==3:
        #点赞
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    else:
        #按照评论的数量排序
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(func.count(CommentModel.id).desc(),PostModel.create_time.desc())
    if board_id:
        query_obj = query_obj.filter(PostModel.board_id==board_id)
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    pagenation = Pagination(bs_version=3,page=page,total=total,outer_window=1,inner_window=2)
    context = {
        'banners' : banners,
        'boards': boards,
        'posts':posts,
        'pagenation':pagenation,
        'currend_board':board_id,
        'current_sort':sort
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
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.parms_error(message=form.get_error())

@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_pdetail.html',post=post)

@bp.route('/acomment/',methods=['POST'])
@login_required
def add_comment():
    form = AddComment(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.parms_error('没有这篇帖子')
    else:
        return restful.parms_error(form.get_error())


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