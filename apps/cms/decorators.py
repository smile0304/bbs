#encoding: utf-8
from flask import session,redirect,url_for
from functools import wraps
import config

def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            session["login_error"] = "操作前请先登录"
            return redirect(url_for('cms.login'))
    return inner

