$(function () {
    $(".highlight-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr('data-id');
        var highlight = parseInt(tr.attr('data-highlight'));
        var url = "";
        if(highlight==1){
            url = '/cms/uhpost/';
        }else{
            url = '/cms/hpost/';
        }
        ttajax.post({
            'url':url,
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data['code']==200){
                    ttalert.alertSuccessToast("操作成功!");
                    setTimeout(function () {
                       window.location.reload();
                    },500);
                }else{
                    ttalert.alertInfo(data['message']);
                }
            }
        });
    });
});