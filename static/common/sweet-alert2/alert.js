var alert = {
    /*
        功能：提示错误
        参数：
            - msg：提示的内容（可选）
    */
    'alertError': function (msg) {
        swal('提示', msg, 'error');
    },

    'alterAddInfor': function () {

        swal.setDefaults({
            input: 'text',
            confirmButtonText: 'Next &rarr;',
            showCancelButton: true,
            animation: false,
            // progressSteps: ['1', '2', '3']
            progressSteps: ['1', '2']
        });

        var steps = [
            {
                title: '输入项目名称',
                text: '输入项目名称的名称'
            },
            '输入项目英文名称',
            // 'Question 3'
        ];

        swal.queue(steps).then(function (result) {
            swal.resetDefaults();
            swal({
                title: '项目已填加成功!',
                html: 'Your answers: <pre>' +
                    JSON.stringify(result) +
                    '</pre>',
                confirmButtonText: '确定',
                showCancelButton: false
            })
        }, function () {
            swal.resetDefaults()
        })
    }
}