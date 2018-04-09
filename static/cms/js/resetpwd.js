
$(function (){
    $("#submit").click(function (event) {
        //阻止表单的默认提交行为
        event.preventDefault();

        //获取表单属性
        var oldpwdE =  $("input[name=oldpwd]");
        var newpwdE =  $("input[name=newpwd]");
        var newpwdE2 =  $("input[name=newpwd2]");
        //获取表单的值
        var oldpwd = oldpwdE.val()
        var newpwd = newpwdE.val()
        var newpwd2 = newpwdE2.val()

        //1.在模板的meta中渲染csrf-token
        //2.在ajax请求的头部设置X-CSRFtoken

        ttajax.post({
            'url':'/cms/resetpwd/',
            'data':{
                'oldpwd':oldpwd,
                'newpwd':newpwd,
                'newpwd2':newpwd2,
            },
            'success':function(data){
                if(data['code'] == 200){
                    ttalert.alertSuccessToast("密码修改成功")
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwdE2.val("");
                }else{
                    var message = data["message"];
                    ttalert.alertError(message);
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwdE2.val("");
                }
            },
            'fail':function (error) {
                ttalert.alertNetworkError();
            }
        })
    })


})