$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var password_input = $("input[name='password']");
        var remember_input = $("inpit[name='remember']");

        var telephone = telephone_input.val();
        var password = password_input.val();
        var remember = remember_input.checked? 1 : 0;


        ttajax.post({
            'url':'/singin/',
            'data':{
                'telephone':telephone,
                'password':password,
                'remember':remember
            },
            'success':function (data) {
                if(data['code']== 200){
                    var renturn_to = $('#return_to_span').text();
                    if(renturn_to){
                        window.location = renturn_to;
                    }else{
                        window.location = '/';
                    }
                }else{
                    ttalert.alertError(data['message']);
                }
            }

        });
    });
});