from flask import Blueprint, render_template, views, request, redirect, url_for, session, send_from_directory, g
from .decorators import front_login_required
from utils import restful
from apps.front.forms import FrontLoginForms, UploadForm, Re_ReleaseForm, DelReleaseForm, EditReleaseForm, ResetPwdForm, \
    ForgotPwdForm, AddProjectForm, DownloadHistoriesAPPForm, ModifyProjectNameForm, delProjectNameForm, \
    RegisterUserForms
from apps.models import ReleaseVersionModel, ProjectLineModel
from apps.front.models import Front_User_models
import config, os, datetime
from sqlalchemy import and_, desc, asc, or_
from exts import db
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from flask_paginate import Pagination, get_page_parameter
from utils import utils

bp = Blueprint('front', __name__)


@bp.route("/")
@front_login_required
def index():
    current_projectId = request.args.get("pd", type=int, default=None)
    AllProjectLine = ProjectLineModel.query.all()
    print(g.projectLine)
    context = {
        'AllProjectLines': AllProjectLine,
        'current_projectId': current_projectId
    }
    return render_template('front/index.html', **context)


class LoginView(views.MethodView):
    def get(self):
        return render_template('front/front_login.html')

    def post(self):
        form = FrontLoginForms(request.form)
        if form.validate():
            loginName = form.telephone.data  # 使用手机号登录
            loginPassword = form.password.data
            remember = form.remember.data
            user = Front_User_models.query.filter_by(telephone=loginName).first()
            if user and user.check_password(loginPassword):
                session[config.FRONT_USER_ID] = user.id
                if remember == 0:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_errors("抱歉登录用户不存在，请确认！！！" or form.get_errors())


# 注册账号
class RegisterView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')

    def post(self):
        form = RegisterUserForms(request.form)
        if form.validate():
            username = form.username.data
            telephone = form.telephone.data
            password = form.password1.data
            email = form.email.data
            user = Front_User_models.query.filter(
                or_(Front_User_models.telephone == telephone, Front_User_models.email == email,
                    Front_User_models.username == username)).first()
            if not user:
                addUser = Front_User_models(username=username, telephone=telephone, password=password, email=email)
                db.session.add(addUser)
                db.session.commit()
                return restful.success()
            else:
                return restful.params_errors("用户已存在，请直接登录")
        else:
            return restful.params_errors(form.get_errors())


# 重置密码
class ResetView(views.MethodView):
    decorators = [front_login_required]

    def get(self):
        return render_template('front/front_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd1.data
            user = g.front_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_errors("旧密码错误")
        else:
            return restful.params_errors(form.get_errors())


@bp.route('/logout/')
@front_login_required
def logout():
    del session[config.FRONT_USER_ID]
    return redirect(url_for('front.login'))


@bp.route('/upload/', methods=['POST'])
@front_login_required
def upload():
    # -------------先修改状态，然后再提交----------------
    signtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:14]
    form = UploadForm(CombinedMultiDict([request.form, request.files]))

    if form.validate():

        apk = form.file.data
        verno = form.verno.data
        desc = form.desc.data
        pid = form.pid.data
        is_commercial = form.is_commercial.data

        ReleaseStatus = ReleaseVersionModel.query.filter_by(projectId=pid, release=1).first()

        # 先将发布状态设置为0， 0表示已下载；1表示已发布并转测试
        if ReleaseStatus and ReleaseStatus.release == 1:
            ReleaseStatus.release = 0
            db.session.commit()

            # 上传新版本并发布
            filename = secure_filename(apk.filename)  # 对中文支持不好
            addTimeFilename = signtime + filename
            apk.save(os.path.join(config.UPLOADED_PATH, addTimeFilename))

            # 解析apk信息
            apkname, apkcode, apkicon = utils.get_apk_information(os.path.join(config.UPLOADED_PATH, addTimeFilename))

            apkVersion = ReleaseVersionModel(appname=addTimeFilename, verNo=verno, descript=desc, projectId=pid,
                                             apkname=apkname, apkcode=apkcode, is_commercial=is_commercial)
            db.session.add(apkVersion)
            db.session.commit()
            return restful.success()
        else:
            # 上传新版本并发布, 没有上传过版本，那么第一次上传必须为新版本
            filename = secure_filename(apk.filename)  # 对中文支持不好
            addTimeFilename = signtime + filename
            apk.save(os.path.join(config.UPLOADED_PATH, addTimeFilename))
            # 解析apk信息, 只限于第一次上传apk需要解析apk icon, 后续则不需要进行解析
            getEngNamePro = ProjectLineModel.query.get(pid)

            apkname, apkcode = utils.parseAPKICO(os.path.join(config.UPLOADED_PATH, addTimeFilename),
                                                 getEngNamePro.project_ename)

            apkVersion = ReleaseVersionModel(appname=addTimeFilename, verNo=verno, descript=desc, projectId=pid,
                                             apkname=apkname, apkcode=apkcode, is_commercial=is_commercial)
            db.session.add(apkVersion)
            db.session.commit()
            return restful.success()
    else:
        return restful.params_errors(form.get_errors())


# 增加项目线
@bp.route('/addproject/', methods=['POST'])
@front_login_required
def add_project():
    form = AddProjectForm(request.form)
    if form.validate():
        pname = form.pname.data
        pEnName = form.pENname.data
        project = ProjectLineModel.query.filter(
            or_(ProjectLineModel.projectName == pname, ProjectLineModel.project_ename == pEnName)).first()
        if not project:
            addProject = ProjectLineModel(projectName=pname, project_ename=pEnName)
            db.session.add(addProject)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_errors("项目重名，请重新输入")
    else:
        return restful.params_errors(form.get_errors())


# 修改项目线(需要传入的参数是中文与英文的名称)
@bp.route('/modifyproject/', methods=['POST'])
@front_login_required
def modifyproject():
    form = ModifyProjectNameForm(request.form)
    if form.validate():
        id = form.id.data
        ch_name = form.pname.data
        # en_name = form.pENname.data
        project = ProjectLineModel.query.get(id)
        project.projectName = ch_name
        # project.project_ename = en_name
        db.session.commit()
        return restful.success()
    else:
        return restful.params_errors(form.get_errors())


# 删除项目线（删除项目线，必须明确当前删除是否要将该项目线下的APK一并删除），该功能请谨慎使用
@bp.route('/delproject/', methods=['POST'])
@front_login_required
def delProject():
    form = delProjectNameForm(request.form)
    if form.validate():
        pid = form.id.data
        Delproject = ProjectLineModel.query.get(pid)
        isAPKList = ReleaseVersionModel.query.filter(ReleaseVersionModel.projectId == pid).all()
        if isAPKList:
            for file in isAPKList:
                delLocalFile = os.path.join(config.UPLOADED_PATH, file.appname)
                apk_file_list = os.listdir(config.UPLOADED_PATH)
                if file.appname in apk_file_list:
                    os.remove(delLocalFile)
                    db.session.delete(file)
                else:
                    db.session.delete(file)

            db.session.delete(Delproject)
            db.session.commit()
            return restful.success()
        else:
            db.session.delete(Delproject)
            db.session.commit()
            return restful.success()

    else:
        return restful.params_errors(form.get_errors())


@bp.route("/<path:projectname>/apkReleaseList/")
@front_login_required
def ReleaseAPK(projectname):
    # 分页处理
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE

    project = ProjectLineModel.query.filter_by(project_ename=projectname).first()
    if project:

        fusionsolarLine = ReleaseVersionModel.query.filter_by(projectId=project.id).order_by(
            desc(ReleaseVersionModel.create_time)).slice(start, end)
        total = ReleaseVersionModel.query.filter_by(projectId=project.id).count()
        pagination = Pagination(page=page, total=total, bs_version=3)

        context = {
            'title': project.projectName,
            'total': total,
            'releases': fusionsolarLine,
            'pagination': pagination
        }
        return render_template('front/front_appRelease.html', **context)
    else:
        return restful.params_errors("不存在该项目")

    # if projectname in config.PRODUCTION_LINE:
    #     fusionsolarLine = ReleaseVersionModel.query.filter_by(projectId=config.PRODUCTION_LINE[projectname]).order_by(
    #         desc(ReleaseVersionModel.create_time)).slice(start, end)
    #     total = ReleaseVersionModel.query.filter_by(projectId=config.PRODUCTION_LINE[projectname]).count()
    #     pagination = Pagination(page=page, total=total, bs_version=3)
    #     context = {
    #         'title': projectname,
    #         'total': total,
    #         'releases': fusionsolarLine,
    #         'pagination': pagination
    #     }


# 可以执行转测试 以及 删除 功能操作
# pname是代表项目名称

@bp.route("/<path:pname>/reupload/", methods=['POST'])
@front_login_required
def reuploadAPK(pname):
    # 产品线
    project = ProjectLineModel.query.filter_by(project_ename=pname).first()
    if project:
        hasReleaseAPP = ReleaseVersionModel.query.filter(ReleaseVersionModel.projectId == project.id,
                                                         ReleaseVersionModel.release == 1).first()
        if hasReleaseAPP:
            hasReleaseAPP.release = 0
            db.session.commit()

            form = Re_ReleaseForm(request.form)
            if form.validate():
                id = form.id.data
                reupload = ReleaseVersionModel.query.get(id)
                if reupload and reupload.release == 0:
                    reupload.release = 1
                    db.session.commit()
                    return restful.success()
                else:
                    return restful.params_errors("对不起，该版本不存在")
            else:
                return restful.params_errors(form.get_errors())
        else:
            return restful.params_errors("没有转测试版本")
    else:
        return restful.params_errors("不存在该产品线")


@bp.route('/editversion/', methods=['POST'])
@front_login_required
def edit_version():
    form = EditReleaseForm(request.form)
    if form.validate():
        id = form.id.data
        remark = form.remark.data
        file = ReleaseVersionModel.query.get(id)
        if file:
            file.remarks = remark
            db.session.commit()
            return restful.success()
        else:
            return restful.params_errors("该版本不存在")
    else:
        return restful.params_errors(form.get_errors())


# 删除版本
@bp.route('/delversion/', methods=['POST'])
@front_login_required
def del_version():
    form = DelReleaseForm(request.form)
    if form.validate():
        id = form.id.data
        file = ReleaseVersionModel.query.filter_by(id=id).first()
        if file and file.release != 1:
            delLocalFile = os.path.join(config.UPLOADED_PATH, file.appname)
            os.remove(delLocalFile)
            db.session.delete(file)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_errors("对不起，文件不存在，或者已发布文件不能被删除")
    else:
        return restful.params_errors(form.get_errors())


@bp.route('/<path:pname>/download/')
def download(pname):
    project = ProjectLineModel.query.filter_by(project_ename=pname).first()
    if project:
        file = ReleaseVersionModel.query.filter(
            and_(ReleaseVersionModel.projectId == project.id,
                 ReleaseVersionModel.release == 1)).first()

        histories = ReleaseVersionModel.query.filter(
            and_(ReleaseVersionModel.projectId == project.id,
                 ReleaseVersionModel.release != 1)).all()
        context = {
            'fileInfor': file,
            'pname': pname,
            'apkname': file.apkname,
            'apkcode': file.apkcode,
            'historiesVersion': histories
        }

        return render_template('front/front_download.html', **context)
    else:
        return restful.params_errors("对不起，没有该产品线，需要联系管理员新建产品线")


# 下载当前转测试版本
@bp.route("/<path:pname>/download/app/")
def downloadFile(pname):
    project = ProjectLineModel.query.filter_by(project_ename=pname).first()
    if project:
        file = ReleaseVersionModel.query.filter(and_(ReleaseVersionModel.projectId == project.id,
                                                     ReleaseVersionModel.release == 1)).first()
        if file:
            return send_from_directory(config.UPLOADED_PATH, file.appname, as_attachment=True)
        else:
            return restful.params_errors("未有版本发布，请联系版本经理！")


@bp.route('/historiesapp/download/<int:id>')
def download_histories_APP(id):
    appid = request.args.get("pd", type=int, default=id)
    file = ReleaseVersionModel.query.get(appid)
    if file:
        return send_from_directory(config.UPLOADED_PATH, file.appname, as_attachment=True)
    else:
        return restful.params_errors("文件不存在")


# 忘记密码
class ForgotPwdView(views.MethodView):
    def get(self):
        return render_template('front/front_forgotpwd.html')

    def post(self):
        form = ForgotPwdForm(request.form)
        if form.validate():
            email = form.email.data
            newpwd = form.password1.data
            # vercode = form.vercode.data
            user = Front_User_models.query.filter_by(email=email).first()
            if user:
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_errors("该用户不存在")
        else:
            return restful.params_errors(form.get_errors())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetView.as_view('resetpwd'))
bp.add_url_rule('/forgotPwd/', view_func=ForgotPwdView.as_view('forgotPwd'))
bp.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
