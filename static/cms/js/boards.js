$(function () {
    $("#add-board-btn").click(function (event) {
        event.preventDefault();
        ttalert.alertOneInput({
            'title':'添加新板块',
            'text':"请输入板块名称",
            'placeholder':'模块名称',
            'confirmCallback':function (inputValue) {
                ttajax.post({
                    'url':'/cms/aboards/',
                    'data':{
                        'name':inputValue
                    },
                    "success":function (data) {
                        if(data['code']==200){
                            window.location.reload();
                        }else{
                            ttalert.alertInfo(data["message"]);
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $('.edit-board-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr("data-id");

        ttalert.alertOneInput({
            'title':'修改板块',
            'text':"请输入板块名称",
            'placeholder':name,
            'confirmCallback':function (inputValue) {
                ttajax.post({
                    'url':'/cms/uboards/',
                    'data':{
                        'board_id':board_id,
                        'name':inputValue
                    },
                    'success':function (data) {
                        if(data['code']==200){
                            window.location.reload();
                        }else{
                            ttalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $(".delete-board-btn").click(function (event) {
    event.preventDefault();
    var self = $(this);
    var tr = self.parent().parent();
    var board_id = tr.attr('data-id');
    ttalert.alertConfirm({
        'msg':"确认删除?",
        'confirmCallback':function () {
            ttajax.post({
                'url':'/cms/dboards/',
                'data':{
                    'board_id':board_id
                },
                'success':function (data) {
                    if(data['code']==200){
                        window.location.reload();
                        ttalert.alertSuccessToast("删除成功");
                    }else{
                        ttalert.alertInfo(data['message']);
                    }
                }
            });
        }
    });

});
});