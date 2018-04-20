
$(function(){
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        if(!email){
            ttalert.alertInfoToast("请输入邮箱");
            return;
        }
        ttajax.get({
            'url':"/cms/email_captcha/",
            'data':{
                'email':email
            },
            'success':function (data) {
                if(data['code'] == 200){
                    ttalert.alertSuccessToast('邮件已成功发送')
                }else{
                    ttalert.alertInfo(data["message"]);
                }
            },
            'fail':function (error) {
                tt.alertNetworkError();
            }
        })
    })
})

$(function () {
    $("#submit").click(function (envent) {
        envent.preventDefault();
        var emailE = $("input[name='email']");
        var captchaE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captchaE.val();

        ttajax.post({
            'url':'/cms/resetemail/',
            'data':{
                'email':email,
                'captcha':captcha
            },
            'success':function (data) {
                if(data['code'] == 200) {
                    ttalert.alertSuccessToast("邮箱修改成功");
                    emailE.val("")
                    captchaE.val("")
                }else{
                    ttalert.alertInfo(data["message"]);
                }
            },
            'fail':function (error) {
                ttalert.alertNetworkError();
            }
        })

    })
})