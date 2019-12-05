from wtforms import Form


# 定义获取表单错误信息
class BaseForm(Form):
    def get_errors(self):
        error_message = self.errors.popitem()[1][0]
        return error_message
