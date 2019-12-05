from flask import jsonify


class HttpCode(object):
    OK = 200
    unauthorerror = 401
    paramserror = 400
    servererror = 500


def restful_result(code, message, data):
    return jsonify({'code': code, 'message': message, 'data': data or {}})


def success(message=None, data=None):
    return restful_result(code=HttpCode.OK, message=message, data=data)


def unauthor_errors(message=None):
    return restful_result(code=HttpCode.unauthorerror, message=message, data=None)


def params_errors(message=None):
    return restful_result(code=HttpCode.paramserror, message=message, data=None)


def server_errors(message=None):
    return restful_result(code=HttpCode.servererror, message=message, data=None)
