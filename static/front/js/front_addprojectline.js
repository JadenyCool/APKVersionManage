// 增加项目线
// $(document).ready(function () {
//     $('#addprojectLine').click(function (event) {
//         event.preventDefault();
//         zlalert.alertOneInput({
//             'title1': '增加项目线中文名称',
//             'title2': '增加项目线英文名称',
//             'placeholder': '项目线名称',
//             'confirmText': '确认添加',
//             'confirmCallback': function (inputValue) {
//                 zlajax.post({
//                     url: '/addproject/',
//                     data: {
//                         'projectname': inputValue,
//                     },
//                     'success': function (data) {
//                         if (data['code'] == 200) {
//                             zlalert.alertSuccessToastWithTime('【' + inputValue + "】 已添加成功", 1000);
//                             setTimeout(function () {
//                                 window.location.href = '/';
//                             }, 1100)
//                         }
//                     },
//                     'fail': function (error) {
//                         zlalert.alertNetworkError();
//                     }
//
//                 })
//             }
//         });
//
//     });
// });


$(function () {
    $('#btn-submit').click(function (event) {
        event.preventDefault();
        var dialog = $('#addproject');

        var pname = $('input[name=pname]').val();
        var pENname = $('input[name=pENname]').val();


        zlajax.post({
            url: '/addproject/',
            data: {
                'pname': pname,
                'pENname': pENname
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    dialog.modal('hide');
                    zlalert.alertSuccessToast("【" + pname + '】项目添加成功')
                    setTimeout(function () {
                        window.location.reload()
                    }, 1200)
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError()
            }
        })

    })
});


// 修改项目
$(function () {
    $('#modifyPro').click(function (event) {
        event.preventDefault();
        // var dialog = $('#addproject');
        // dialog.modal('show');

        var self = $('#Pmenubar');
        var id = parseInt(self.attr('data-id'));
        var CHname = self.attr('data-CHname');
        var Ename = self.attr('data-Ename');

        var pnameInput = $('input[name=pname]');
        var pENnameInput = $('input[name=pENname]');

        //向输入框增加值
        pnameInput.val(CHname);
        pENnameInput.val(Ename);

        zlalert.alertOneInput({
            'title': "修改项目名称",
            'placeholder': CHname,
            'confirmText': '确认修改',
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    url: "/modifyproject/",
                    data: {
                        'id': id,
                        'pname': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            zlalert.alertSuccess("名称已修改", function () {
                                window.location.reload()
                            })

                        }
                    }
                })
            }
        })
    })
});


// 删除项目（需要删除项目下所有版本）
$(function () {
    $('#delP').click(function (event) {
        event.preventDefault();

        var self = $('#Pmenubar');
        var id = parseInt(self.attr('data-id'));

        zlalert.alertConfirm({
            'title': '删除项目',
            'msg': "确定要删除该项目？如果【确认】删除该项目，将默认删除所有该项目下所有版本，请谨慎操作！",
            'confirmText': '确认',
            'cancelText': '取消',
            'confirmCallback': function () {
                zlajax.post({
                    url: "/delproject/",
                    data: {
                        'id': id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            zlalert.alertSuccessToast('修改成功');
                            window.location.reload()
                        }
                    },
                    'fail': function (error) {
                        zlalert.alertNetworkError()
                    }
                })
            }
        })

    })
});