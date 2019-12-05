from flask import Flask
from flask_wtf import CSRFProtect

import config
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from exts import db, mail

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
CSRFProtect(app)

# 注册蓝图前端页面
app.register_blueprint(front_bp)
app.register_blueprint(common_bp)

if __name__ == '__main__':
    app.run()
