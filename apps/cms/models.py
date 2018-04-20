#encoding: utf-8

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class CMSPersmisson(object):

    #以255的二进制方式表示权限 1111 1111
    All_PERMISSION = 0b11111111 #拥有所有权限
    VISITOR =        0b00000001 #访问者权限
    POSTER =         0b00000010 #帖子管理权限
    COMMENTER =      0b00000100 #评论管理权限
    BORDER =         0b00001000 #管理板块权限
    FRONTUSER =      0b00010000 #管理前台用户权限
    CMSUSER =        0b00100000 #管理后台用户的权限
    ADMINER =        0b01000000 #管理后台管理员

cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)

)

class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200),nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    permissions = db.Column(db.Integer,default=CMSPersmisson.VISITOR)

    users = db.relationship('CMSUser',secondary=cms_role_user,backref='roles')


class CMSUser(db.Model):

    __tablename__ = 'cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password= generate_password_hash(raw_password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result

    @property
    def permission(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
            return all_permissions

    def has_permission(self,permission):
        # all_permissions = self.permissions
        # result = all_permissions & permission == permission
        # return result
        return self.permission & permission == permission

    @property
    def is_developer(self):
        return self.has_permission(CMSPersmisson.All_PERMISSION)