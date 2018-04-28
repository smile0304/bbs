$(function () {
    var ue = UE.getEditor("ueditor",{
        'server_url':'/ueditor/upload/',
        "toolbars": [
            [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'source', //源代码
                'blockquote', //引用
                'selectall', //全选
                'insertcode', //代码语言
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传
                'emotion' //表情
            ]
        ]
    });
    window.ue = ue;
});

$(function () {
    $("#comment-btn").click(function (event) {
        event.preventDefault();
        var loginTag = parseInt($('#login-tag').attr("data-is-login"));
        if(loginTag!=1){
            window.location = '/singin/';
        }else{
            var content = window.ue.getContent();
            var post_id = $("#post-content").attr("data-id");
            ttajax.post({
                'url':'/acomment/',
                'data':{
                    'content':content,
                    'post_id':post_id,
                },
                'success':function (data) {
                    if(data['code']==200){
                        ttalert.alertSuccessToast("评论发表成功");
                        setTimeout(function () {
                            window.location.reload();
                        },500);
                    }else{
                        ttalert.alertInfo(data["message"]);
                    }
                }
            });
        }
    });
});
