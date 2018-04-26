$(function () {
    var ue = UE.getEditor("editor",{
        "serverUrl":"/ueditor/upload/"
    });
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $('input[name="title"]');
        var boardSelect = $('Select[name="board_id"]');
        var title = titleInput.val();
        var board_id = boardSelect.val();

        var content = ue.getContent();

        ttajax.post({
            'url':'/apost/',
            'data':{
                'title':title,
                'content':content,
                'board_id':board_id
            },
            'success':function (data) {
                if(data['code']==200){
                    ttalert.alertConfirm({
                        'msg':"恭喜,帖子发表成功!",
                        'cancelButtonText':'index',
                        'confirmText':'againt',
                        'cancelText':function () {
                            window.location = '/'
                        },
                        'confirmCallback':function () {
                            titleInput.val("");
                            ue.setContent("");
                        }
                    });
                }else{
                    ttalert.alertError(data['message']);
                }
            }
        });

    });
});