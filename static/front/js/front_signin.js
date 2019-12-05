$(function () {
    $('#submit-signin-btn').click(function (event) {
        event.preventDefault()
        var telephoneE = $('input[name=telephone]');
        var passwordE = $('input[name=password]');
        var rememberE = $('input[name=remember]');


        var telephone = telephoneE.val();
        var password = passwordE.val();
        var remember = rememberE.checkbox?1:0;

        zlajax.post({
            'url': "/login/",
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember
            },
            'success': function (data) {
                if (data["code"] == 200) {
                    window.location.href = '/'
                }
                else {
                    zlalert.alertError("用户名或者密码不正确")
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError()
            }
        })
    })

});