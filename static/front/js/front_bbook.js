$(function () {
    $(".borrow-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent().parent();

        var bookid = tr.attr('data-id');
        // var deviceinhome = parseInt(tr.attr('data-inhome'));

        zlajax.post({
            'url': "/bbook/",
            'data': {
                'bookid': bookid
                // 'inhome': deviceinhome
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast("该书已成功借用");
                    setTimeout(function () {
                        window.location.reload()
                    }, 500)

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
            'title': '书籍归还',
            'msg': "请确认书籍无破损",
            'confirmCallback': function () {
                window.location.reload()
            }
        })
    })
});

