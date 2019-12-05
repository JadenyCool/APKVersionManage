from exts import db
from werkzeug.security import check_password_hash, generate_password_hash
import shortuuid
from datetime import datetime


class Front_User_models(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(50), primary_key=True, default=shortuuid.uuid)
    username = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, telephone, email):
        self.username = username
        self.password = password
        self.telephone = telephone
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, rawpassword):
        self._password = generate_password_hash(rawpassword)

    # 检查密码
    def check_password(self, newpassword):
        result = check_password_hash(self.password, newpassword)
        return result

