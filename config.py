#encoding: utf-8
import os

DEBUG = True
SECRET_KEY = os.urandom(24)
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'bbs'
"""
设置session过期时间
PERMANENT_SESSION_LIFETIME = 10(秒)
"""
DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = "abcacb"

#邮箱配置
MAIL_SERVER = "smtp.163.com"
MAIL_PORT = '25'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "18860057945@163.com"
MAIL_PASSWORD = "qwertyuiop1234"
MAIL_DEFAULT_SENDER = "18860057945@163.com"
