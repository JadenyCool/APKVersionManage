$('form').on('submit', function (event) {
    // 显示进度条
    $('.progress').css('display', 'block');
    // 阻止元素发生默认的行为，此处用来阻止对表单的提交
    event.preventDefault();

    //获取projectID
    var projectID = $('#pid');
    var pid = parseInt(projectID.attr('data-id'));

    var formData = new FormData(this);
    formData.set('pid', pid);
    // jQuery Ajax 上传文件，关键在于设置：processData 和 contentType
    $.ajax({
        xhr: function () {
            var xhr = new XMLHttpRequest();
            xhr.upload.addEventListener('progress', function (e) {
                if (e.lengthComputable) {
                    var percent = Math.round(e.loaded * 100 / e.total);
                    $('.progress-bar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
                }
            });
            return xhr;
        },
        type: 'POST',
        url: '/upload/',
        cache: false,
        data: formData,
        // 告诉 jQuery 不要去处理发送的数据
        processData: false,
        // 告诉 jQuery 不要去设置 Content-Type 请求头
        // 因为这里是由 <form> 表单构造的 FormData 对象，且已经声明了属性 enctype="multipart/form-data"，所以设置为 false
        contentType: false
    }).done(function (res) {
        zlalert.alertSuccess("文件上传成功!", function () {
            window.location.reload();
        });

    }).fail(function (res) {
        zlalert.alertError("文件上传失败，请重新上传")
    });
});


//【转测】试版本功能
$(function () {
    $('.re-release').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var versionId = tr.attr('data-id');

        var url = '';
        // var getUrl = window.location.href;
        var getPathname = window.location.pathname;
        var Url_key = getPathname.split("/")[1];

        url = "/" + Url_key + "/reupload/";


        // if (getUrl.includes('fusionsolar')) {
        //     url = '/fusionsolar/reupload/';
        // } else if (getUrl.includes('icleanpower')) {
        //     url = '/icleanpower/reupload/';
        // } else if (getUrl.includes('eHome')) {
        //     url = '/eHome/reupload/';
        // } else if (getUrl.includes('ptm')) {
        //     url = '/ptm/reupload/';
        // } else if (getUrl.includes('okr')) {
        //     url = '/okr/reupload/';
        // } else if (getUrl.includes('atesi')) {
        //     url = '/atesi/reupload/';
        // }

        zlajax.post({
            'url': url,
            'data': {
                'id': versionId
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccess("该版本已转测成功，请通知测试进行版本测试！", function () {
                        window.location.reload();
                    });
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError()
            }
        })
    })
});


// 编辑版本信息（不能上传文件）
$(function () {
    $('.editversion').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var versionId = tr.attr('data-id');
        var remarks = tr.attr('data-remarks');

        zlalert.alertOneInput({
            'title': "增加备注",
            'placeholder': remarks,
            'confirmText': '确认修改',
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    url: "/editversion/",
                    data: {
                        'id': versionId,
                        'remark': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            zlalert.alertSuccess("已成功添加备注信息", function () {
                                window.location.reload()
                            })

                        }
                    }
                })
            }
        })
    })
});


// 【删除】版本
$(function () {
    $('.del-version').click(function (event) {
        event.preventDefault();
        var self = $(this);

        var tr = self.parent().parent();

        var delVersionId = tr.attr('data-id');

        zlalert.alertConfirm({
            'title': '版本删除确认',
            'msg': '你确定要删除该版本吗？',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/delversion/',
                    'data': {
                        'id': delVersionId
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload()
                        }
                    },
                    'fail': function (error) {
                        zlalert.alertInfo(data['message'])
                    }
                })
            }
        })
    })
});


//浏览功能
$(function () {
    $('.app-brower').click(function (event) {
        event.preventDefault();
        //获取当前浏览器的地址
        // var url = '';
        // var getUrl = window.location.href;
        var down_url = '';
        var getUrl = window.location.pathname;
        var url_key = getUrl.split("/")[1];

        down_url = "/" + url_key + "/download/";
        window.location.href = down_url;

        // if (getUrl.includes('fusionsolar')) {
        //
        //     window.location.href = '/fusionsolar/download/'
        // } else if (getUrl.includes('icleanpower')) {
        //     window.location.href = '/icleanpower/download/';
        // } else if (getUrl.includes('eHome')) {
        //     window.location.href = '/eHome/download/';
        // } else if (getUrl.includes('ptm')) {
        //     window.location.href = '/ptm/download/';
        // } else if (getUrl.includes('okr')) {
        //     window.location.href = '/okr/download/';
        // } else if (getUrl.includes('atesi')) {
        //     window.location.href = '/atesi/download/';
        // }

    })
});
