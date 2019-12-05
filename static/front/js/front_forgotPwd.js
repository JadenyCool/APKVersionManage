// 发送邮件验证码
$(function () {
    $("#send-email-captcha-btn").click(function (event) {
        event.preventDefault();
        var email = $('input[name=email]').val();

        var getemailDomain = email.split('@')[1];

        if (getemailDomain != 'pinnettech.cn') {
            zlalert.alertError("该邮箱地址不属于公司邮箱地址，因此无法获取验证码，请联系管理修改")

        } else {
            zlajax.post({
                url: '/c/send_email_capcha/',
                data: {
                    'email': email
                },
                'success': function (data) {
                    if (data['code'] == 200) {
                        zlalert.alertSuccessToast("验证码发送成功！")
                    }
                },
                'fail': function (error) {
                    zlalert.alertNetworkError()
                }
            })
        }
    })
});


//提交修改密码：
$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();

        var email = $('input[name=email]').val();
        var capcha = $('input[name=vercode]').val();
        var password1 = $('input[name=password1]').val();
        var password2 = $('input[name=password2]').val();

        zlajax.post({
            url: '/forgotPwd/',
            data: {
                'email': email,
                'vercode': capcha,
                'password1': password1,
                'password2': password2
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToastWithTime("密码修改成功,即将跳转登录界面", 3000);
                    setTimeout(function () {
                        window.location.href = '/';
                    }, 3500)
                } else {
                    zlalert.alertError(data['message'])
                }

            },
            'fail': function (error) {
                zlalert.alertNetworkError()
            }
        })
    })
});