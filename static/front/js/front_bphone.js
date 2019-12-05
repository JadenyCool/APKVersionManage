$(function () {
    $(".borrow-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent().parent();

        var phone_id = tr.attr('data-id');
        var deviceinhome = parseInt(tr.attr('data-inhome'));

        zlajax.post({
            'url': "/bphone/",
            'data': {
                'phone_id': phone_id,
                'inhome': deviceinhome
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast("手机已成功借用");
                    setTimeout(function () {
                        window.location.reload()
                    },500)

                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError()
            }
        })
    })
});


//点击归还
$(function () {
    $('.back-btn').click(function (event) {
        zlalert.alertConfirm({
            'title': '手机归还',
            'msg':"手机请关机交由管理员处，并由管理确认该次手机借还记录",
            'confirmCallback': function () {
                window.location.reload()
            }
        })
    })
});

