#encoding: utf-8
from flask import session,redirect,url_for,request,g
from functools import wraps
import config


def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            session["login_info"] = "操作前请先登录"
            return redirect(url_for('cms.login',next=request.url))
    return inner

def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args,**kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter
