import os
from apps.models import ReleaseVersionModel, ProjectLineModel

# 数据库配置

# DEBUG = True

# config databases
HOST = '127.0.0.1'
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'PinnetRelease'
PORT = '3306'

SQL_URL = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8'.format(username=USERNAME,
                                                                                         password=PASSWORD
                                                                                         , host=HOST,
                                                                                         port=PORT,
                                                                                         db=DATABASE)

SQLALCHEMY_DATABASE_URI = SQL_URL

SQLALCHEMY_TRACK_MODIFICATIONS = False

TEMPLATES_AUTO_RELOAD = True

# session会话
SECRET_KEY = os.urandom(24)

CMS_USER_ID = 'adfdasfdjksafdiasoffjijkd'

FRONT_USER_ID = 'kkladfdsafjdsfdsfjlkk12345525'

# config page can display post number at every pages
PER_PAGE = 10

# upload file path
# https://flask-dropzone.readthedocs.io/en/latest/configuration.html#file-type-filter

basedir = os.path.abspath(os.path.dirname(__file__))
# apk upload file path
UPLOADED_PATH = os.path.join(basedir, 'ReleaseVersion')

# parse .apk icon path
PARSE_APKICON_TOOLS_PATH = os.path.join(basedir, 'bin/')
SAVE_APKICON_PATH = os.path.join(basedir, 'static/images/')

# DROPZONE_ALLOWED_FILE_CUSTOM = True  #允许自定义后续类型
# DROPZONE_ALLOWED_FILE_TYPE = '.apk'
# DROPZONE_MAX_FILE_SIZE = 300
# DROPZONE_MAX_FILES = 1
# DROPZONE_ENABLE_CSRF = True  # enable CSRF protection


# 版本发布分页
VERSION_PAGE = 10

# config Email
MAIL_SERVER = 'XXXXXXX'
MAIL_PORT = 25
MAIL_USERNAME = 'XXXXXXXX'
MAIL_PASSWORD = "XXXXXXX"  # 邮箱授权码，不是邮箱密码
MAIL_DEFAULT_SENDER = 'XXXXXXXX'


