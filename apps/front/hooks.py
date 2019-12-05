from flask import session, g

import config
from apps.models import ProjectLineModel
from .models import Front_User_models
from .views import bp


# 处理前台登录后显示用户名

@bp.before_request
def before_request():
    if config.FRONT_USER_ID in session:
        userid = session.get(config.FRONT_USER_ID)
        user = Front_User_models.query.get(userid)
        if user:
            g.front_user = user
            project = ProjectLineModel.query.all()
            g.projectLine = project