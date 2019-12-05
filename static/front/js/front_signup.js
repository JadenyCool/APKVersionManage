// $(function () {
//     $("#captcha-img").click(function (event) {
//         var self = $(this);
//         var src = self.attr("src");
//         var newsrc = zlparam.setParam(src, 'xxx', Math.random());
//         self.attr('src', newsrc)
//
//     })
//
// });

//send SMS captcha
// $(function () {
//     $("#send-captcha-btn").click(function (event) {
//         event.preventDefault();
//         var self = $(this);
//         var telephone = $('input[name=telephone]').val();
//        if(!(/^1[345879]\d{9}$/.test(telephone))){
//             zlalert.alertInfoToast('请输入正确的手机号码！');
//             return;
//         }
//        zlajax.get({
//            "url":"/c/sms/captcha?telephone="+telephone,
//            "success":function (data) {
//                if(data['code']==200){
//                    zlalert.alertSuccessToast('短信验证码发送成功')
//                    self.attr('disabled', 'disabled');
//                    //倒计时
//                    var timecount = 60;
//                   var timer = setInterval(function () {
//                         timeout--;
//                         self.text(timecount);
//                         if (timecount <= 0){
//                             self.removeAttr('disabled');
//                             clearInterval(timer);
//                             self.text('发送验证码')
//
//                         }
//                    },1000)
//                }else{
//                    zlalert.alertInfo("验证码发送失败")
//                }
//
//            }
//        })
//     })
// });

$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var telephoneE = $('input[name=telephone]');
        var usernameE = $('input[name=username]');
        var emailE = $('input[name=email]');
        var password1E = $('input[name=password1]');
        var password2E = $('input[name=password2]');
        // var img_catpchaE = $('input[name=img_catpcha]');


        var telephone = telephoneE.val();
        var username = usernameE.val();
        var email = emailE.val();
        var password1 = password1E.val();
        var password2 = password2E.val();
        // var img_catpcha = img_catpchaE.val();

        zlajax.post({
            'url': "/register/",
            'data': {
                'telephone': telephone,
                'username': username,
                'email': email,
                'password1': password1,
                'password2': password2,
                // 'img_catpcha': img_catpcha
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast("您已注册成功");
                    setTimeout(function () {
                        window.location = '/'
                    }, 700)
                }else{
                    // zlalert.alertInfo(data['message']);
                    zlalert.alertConfirm({
                        'msg':data['message'],
                        'confirmText':"返回登录",
                        "confirmCallback":function () {
                            window.location = '/'
                        }

                    })
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError()
            }
        })


    })
});