$('#passwordConfirm, #inputPassWord').focusout(
    function () {
        var PassWord = $('#inputPassWord').val();
        var PassWord2 = $('#passwordConfirm').val();
        if (PassWord && PassWord2 && PassWord2 != PassWord){
            $(this).siblings('span').text('两次密码不一致');
        }
        else {
            $(this).siblings('span').text('');
        }
    }
);


(function (jq) {

    jq.extend({
        loginCheck: function () {
            $('#login-btn, #reg-btn').click(function () {
                var flag = true;
                $('input').siblings('span').text('');
                $('input').each(function (k, v) {
                    if ($(v).val()){
                        $(v).siblings('span').text('');
                    }
                    else {
                        if ($(v).attr('null')){}
                        else {
                            $(v).siblings('span').text($(this).prop('placeholder'));
                            console.log(flag);
                            flag = false;
                            return false
                        }
                    }
                });
                var PassWord = $('#inputPassWord').val();
                var PassWord2 = $('#passwordConfirm').val();

                if (PassWord && PassWord2 && PassWord != PassWord2){
                    flag = false;
                    $('#passwordConfirm').siblings('span').text('两次密码不一致');
                }
                console.log(flag);
                return flag

            })
        }
    });
})(jQuery);