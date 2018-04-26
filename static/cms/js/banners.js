$(function () {
    $("#test").click(function (event) {
        event.preventDefault();
        var savebtn = $("#save-banner-btn");
        savebtn.removeAttr("data-type");
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name='name']");
        var imageInput = $("input[name='image_url']");
        var linkInput = $("input[name='link_url']");
        var priorityInput = $("input[name='priority']");


        var name = nameInput.val("");
        var image_url = imageInput.val("");
        var link_url = linkInput.val("");
        var priority = priorityInput.val("");
    });
});

$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name='name']");
        var imageInput = $("input[name='image_url']");
        var linkInput = $("input[name='link_url']");
        var priorityInput = $("input[name='priority']");


        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();
        var submitType = self.attr('data-type');
        var bannerId = self.attr("data-id");

        if(!name || !image_url || !link_url || !priority){
            ttalert.alertInfoToast('请输入完整的轮播图数据！');
            return;
        }

        var url = '';
        if(submitType == 'update'){
            url = '/cms/ubanner/';
        }else{
            url = '/cms/abanner/';
        }

        ttajax.post({
            "url": url,
            'data':{
                'name':name,
                'image_url': image_url,
                'link_url': link_url,
                'priority':priority,
                'banner_id': bannerId
            },
            'success': function (data) {
                dialog.modal("hide");
                if(data['code'] == 200){
                    // 重新加载这个页面
                    window.location.reload();
                }else{
                    ttalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                ttalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    $(".edit-banner-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");

        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr("data-type",'update');
        saveBtn.attr('data-id',tr.attr('data-id'));
    });
});

$(function () {
    $(".delect-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        ttalert.alertConfirm({
            "msg" : "确定删除?",
            'confirmCallback':function () {
                ttajax.post({
                    'url':'/cms/dbanner/',
                    'data':{
                        'banner_id': banner_id,
                    },
                    'success':function (data) {
                        if(data['code']==200){
                            window.location.reload();
                            ttalert.alertSuccessToast("删除成功");
                        }else{
                            ttalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});

$(function () {
    ttqiniu.setUp({
        'domain': 'http://file.smilehacker.net/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/c/uptoken/',
        'success': function (up,file,info) {
            var imageInput = $("input[name='image_url']");
            imageInput.val(file.name);
        }
    });
});