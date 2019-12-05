from apps.forms import BaseForm
from wtforms.fields import StringField, IntegerField, FileField, TextAreaField
from wtforms.validators import InputRequired, Email, Regexp, EqualTo, ValidationError
from flask_wtf.file import FileRequired, FileAllowed
from utils import zlcache


# 登录验证器
class FrontLoginForms(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='请输入正确格式的手机号码！')])
    password = StringField(validators=[InputRequired(message="请输入密码")])
    remember = IntegerField()


class RegisterUserForms(BaseForm):
    username = StringField(validators=[InputRequired(message='请输入用户名')])
    password1 = StringField(validators=[InputRequired(message="请输入密码"), Regexp(r".{6,20}", message='密码长度不够，6-20位')])
    password2 = StringField(validators=[EqualTo('password1', message="两次输入的密码不一样")])
    telephone = StringField(
        validators=[InputRequired(message="请输入手机号"), Regexp(r"1[345789]\d{9}", message='请输入正确格式的手机号码！')])
    email = StringField(validators=[Email(message='请输入正确的邮箱地址')])


# 重置密码
class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[InputRequired(message='旧密码不能为空')])
    newpwd1 = StringField(validators=[InputRequired(message='新密码不能为空'), Regexp(r".{6,20}", message='密码长度不够，6-20位')])
    newpwd2 = StringField(
        validators=[EqualTo('newpwd1', message="两次输入的密码不相同，请重新输入"), Regexp(r".{6,20}", message='密码长度不够，6-20位')])


# 版本发布验证
class UploadForm(BaseForm):
    file = FileField(validators=[FileRequired(), FileAllowed(['apk', 'ipa'])])
    pid = IntegerField(validators=[InputRequired(message="必须输入apk所属于项目id")])
    verno = StringField(validators=[InputRequired(message="迭代版本号是必须要输入")])
    is_commercial = IntegerField(validators=[InputRequired(message='版本是否为商用还是转测试版本的信息不能为空')])
    desc = TextAreaField()


class Re_ReleaseForm(BaseForm):
    id = IntegerField(validators=[InputRequired(message="请传入需要重新上架的版本ID")])


class DelReleaseForm(BaseForm):
    id = IntegerField(validators=[InputRequired(message="请传入需要删除的版本ID")])


class EditReleaseForm(BaseForm):
    id = IntegerField(validators=[InputRequired(message="请传入需要编辑的版本ID")])
    remark = StringField()


# 添加项目线
class AddProjectForm(BaseForm):
    pname = StringField(validators=[InputRequired(message="请输入项目线名称")])
    pENname = StringField(validators=[InputRequired(message="请输入项目线英文名称且不能带空格")])


# 修改项目名称(需要修改项目的中文名称以及英文名称， 调用模态对话框)
class ModifyProjectNameForm(BaseForm):
    id = IntegerField(validators=[InputRequired(message="未获取到项目ID编号")])
    pname = StringField(validators=[InputRequired(message="请输入项目线名称")])


# 删除项目线（需要删除以及其下的所有版本）
class delProjectNameForm(BaseForm):
    id = IntegerField(validators=[InputRequired(message="未获取到项目ID编号")])


# 下载历史版本
class DownloadHistoriesAPPForm(BaseForm):
    id = IntegerField(validators=[InputRequired(message="请传入下载版本ID")])


# 忘记密码
class ForgotPwdForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱地址')])
    password1 = StringField(validators=[InputRequired(message='新密码不能为空'), Regexp(r".{6,20}", message='密码长度不够，6-20位')])
    password2 = StringField(
        validators=[EqualTo('password1', message="两次输入的密码不相同，请重新输入"), Regexp(r".{6,20}", message='密码长度不够，6-20位')])
    vercode = StringField(validators=[InputRequired(message="验证码不能为空")])

    def vercode_validator(self, field):
        vercode = field.data
        email = self.email.data
        capcha_cache = zlcache.get(email)
        if not vercode or vercode.lower() != capcha_cache.lower():
            raise ValidationError("验证码错误！" + vercode.lower() + "和" + capcha_cache.lower())
