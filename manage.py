#encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import create_app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel,BoardModel,PostModel

app = create_app()
CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPersmisson

FrontUser = front_models.FrontUser
manager = Manager(app)

Migrate(app,db)
manager.add_command('db',MigrateCommand)


@manager.option('-u','--username',dest="username")
@manager.option('-p','--password',dest="password")
@manager.option('-e','--email',dest="email")
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print("用户添加成功")


@manager.command
def create_role():
    #访问者权限
    vistor = CMSRole(name="访问者",desc='只能访问个人信息，不能修改')
    vistor.permissions = CMSPermission.VISITOR

    #运营权限
    operator = CMSRole(name="运营",desc="管理帖子，管理评论,管理前台用户")
    operator.permissions = CMSPermission.VISITOR | CMSPermission.POSTER |\
        CMSPermission.COMMENTER | CMSPermission.FRONTUSER

    #管理员
    admin = CMSRole(name="管理员",desc="拥有所有权限")
    admin.permissions = CMSPermission.VISITOR | CMSPermission.POSTER |\
        CMSPermission.COMMENTER | CMSPermission.BORDER | CMSPermission.FRONTUSER |\
        CMSPermission.CMSUSER

    #开发者 超级管理员
    develpoer = CMSRole(name="开发者",desc="开发人员专用")
    develpoer.permissions = CMSPermission.All_PERMISSION

    db.session.add_all([vistor,operator,admin,develpoer])
    db.session.commit()

@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()
    print("用户添加成功")


@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("用户添加到角色成功!")
        else:
            print("角色:%s 不存在!" % role)
    else:
        print("用户:%s 不存在!"% email)

@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print("这个用户有访问者权限")
    else:
        print("没有访问者权限")
@manager.command
def create_test_post():
    for x in range(1,205):
        title = "标题%s" %x
        content = "内容%s" %x
        board = BoardModel.query.first()
        anthor = FrontUser.query.first()
        post = PostModel(title=title,content=content)
        post.board = board
        post.author = anthor
        db.session.add(post)
        db.session.commit()
    print("测试用例添加成功")

if __name__ == '__main__':
    manager.run()