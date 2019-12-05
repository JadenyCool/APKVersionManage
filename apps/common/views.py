import random
import string
from io import BytesIO

from flask import Blueprint, request, make_response
from flask_mail import Message
from flask_qrcode import qrc
# from utils.captcha import Captcha
from apps.models import ProjectLineModel
import config
from exts import mail
from utils import restful
from utils import zlcache

bp = Blueprint('common', __name__, url_prefix="/c")


# @bp.route('/sms/captcha/')
# def sms_captcha():
#     telephone = request.args.get("telephone")
#     if not telephone:
#         return restful.param_error("请传入手机号码")
#     captcha = Captcha.gene_text(4)
#     if alidayu.send_sms(telephone, code=captcha):
#         return restful.success()
#     else:
#         return restful.param_error("短信验证码发送失败")


# @bp.route('/capcha/')
# def grap_capcha():
#     # 获取验证码
#     text, image = Captcha.gene_graph_captcha()
#
#     zlcache.set(text.lower(), text.lower())  # 将图形验证码放到缓存服务器上
#
#     # ByteIO:自戴留
#     out = BytesIO()
#     image.save(out, 'png')
#     out.seek(0)
#     resp = make_response(out.read())
#     resp.content_type = 'image/png'
#     return resp


@bp.route("/send_email_capcha/", methods=['POST'])
def send_email_capcha():
    email = request.form.get('email')
    if not email:
        return restful.params_errors("请输入邮箱地址")
    else:
        source = list(string.ascii_letters + string.digits)
        emailCapcha = "".join(random.sample(source, 6))
        message = Message(subject="品联APK管理平台-邮箱验证码", recipients=[email],
                          body="当前验证码为：{}， 该验证码有效期为5分钟".format(emailCapcha),
                          sender=config.MAIL_DEFAULT_SENDER)
        try:
            mail.send(message)
            zlcache.set(email, emailCapcha)
            return restful.success()
        except:
            return restful.server_errors()


# send email test
# @bp.route('/testmail/')
# def test_mail():
#     message = Message("学习邮件发送", recipients=['gulinjie@pinnettech.cn'], body="邮件发送")
#     mail.send(message)
#     return restful.success()


@bp.route('/<path:pname>/qr/')
def qrcode(pname):
    project = ProjectLineModel.query.filter_by(project_ename=pname).first()
    if project:
        link = request.url.replace('/c', "").replace('/qr', "") + 'download/app'
        image = qrc.make(link)
        out = BytesIO()
        image.save(out, 'png')
        out.seek(0)
        resp = make_response(out.read())
        resp.content_type = 'image/png'
        return resp
    else:
        return


@bp.route('/checkPLine/')
def checkPLine():
    ProjectLine = ProjectLineModel.query.with_entities(ProjectLineModel.projectName)
    print(type(ProjectLine))
    print(ProjectLine)
    return restful.success()
