$(function () {
   $('#submit-btn').click(function (event) {
       event.preventDefault();
       var oldpwdE = $('input[name=oldpwd]');
       var newpwd1 = $('input[name=newpwd1]');
       var newpwd2 = $('input[name=newpwd2]');

       var oldpwd = oldpwdE.val();
       var newpwd1 = newpwd1.val();
       var newpwd2 = newpwd2.val();

       zlajax.post({
           'url':'/resetpwd/',
           'data': {
               'oldpwd': oldpwd,
               'newpwd1': newpwd1,
               'newpwd2': newpwd2
           },
           'success': function (data) {
               if(data['code'] == 200){
                 zlalert.alertSuccess("密码修改成功,请重新登录", function () {
                     window.location.href = '/login/'
                 })
               }else{
                   zlalert.alertError(data['message'])
               }
           },
           'fail': function (error) {
               zlalert.alertNetworkError()
           }
       })

   })
});