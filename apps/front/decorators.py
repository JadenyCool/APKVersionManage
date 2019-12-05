from functools import wraps
from flask import session, redirect, url_for
import config


# 登录需要
def front_login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config.FRONT_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.login'))

    return inner
