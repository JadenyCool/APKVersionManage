from exts import db
from datetime import datetime
from sqlalchemy import desc, asc


# 先建立产品线
class ProjectLineModel(db.Model):
    __tablename__ = 'project_line'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectName = db.Column(db.String(100), nullable=False)
    project_ename = db.Column(db.String(100), nullable=False)


# 发布APP版本并通过外键关联产品线
class ReleaseVersionModel(db.Model):
    __tablename__ = 'releaseVersion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    verNo = db.Column(db.String(50), nullable=False)
    descript = db.Column(db.Text)
    appname = db.Column(db.String(100), nullable=False)
    release = db.Column(db.Integer, nullable=False, default=1)  # 0表示不发布，1表是发布
    apkname = db.Column(db.String(100))  # 直接通过上传获取apk包内的appname
    apkcode = db.Column(db.String(10))  # 直接通过上传获取apk包内的vercode
    projectId = db.Column(db.Integer, db.ForeignKey('project_line.id'))
    remarks = db.Column(db.String(100))
    is_commercial = db.Column(db.Integer)  # 是否为商用版本，或者是转测试版本
    create_time = db.Column(db.DateTime, default=datetime.now)

    __mapper_args__ = {
        'order_by': desc(create_time)
    }
