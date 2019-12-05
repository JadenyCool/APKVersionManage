from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app
from exts import db
from apps.front import models as front_models
from apps.models import ReleaseVersionModel, ProjectLineModel

front_user = front_models.Front_User_models
releaseVersion = ReleaseVersionModel

manage = Manager(app)
Migrate(app, db)

manage.add_command('db', MigrateCommand)


# 给管理员增加超级账号权限
@manage.option('-u', '--username', dest='username')
@manage.option('-t', '--telephone', dest='telephone')
@manage.option('-e', '--email', dest='email')
@manage.option('-p', '--password', dest='password')
def add_front_user_command(username, email, password, telephone):
    checkuser = front_user.query.filter_by(email=email).first()
    if not checkuser:
        user = front_user(username=username, email=email, password=password, telephone=telephone)
        db.session.add(user)
        db.session.commit()
        print('用户新增加成功')
    else:
        print('已有该用户存在，增加失败')


if __name__ == '__main__':
    manage.run()
