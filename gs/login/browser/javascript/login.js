jQuery.noConflict();

function gs_login_submit (event) {
    var el = null, 
        pw = null, 
        encrypt = null, 
        loginText = null, 
        seed = null, 
        new_passvalue = null;
    el = jQuery('#login-form');
    pw = jQuery('#password').val();
    encrypt = jQuery('#ep').val();

    if (encrypt == 'True') {
        pw = b64_sha1(pw);
    }
    loginText = jQuery('#login').val();
    seed = jQuery('#seed').val();
    new_passvalue = hex_hmac_sha1(pw, (loginText+pw+seed));
    jQuery('#ph').val(new_passvalue);
    jQuery('#password').val('');
    //Event.unloadCache();
} // loginSubmit

function gs_login_init () {
    jQuery('#login-form').submit(gs_login_submit);
}

function gs_login_toggle_init () {
    var toggler = null;
    toggler = GSProfilePasswordToggle('#password',
                                      '#gs-login-password-toggle-widget');
}

jQuery(window).load( function() {
    jQuery('#login').focus();
    gsJsLoader.with_module("/++resource++crypto-20130402/sha1-min.js", 
                           gs_login_init);
    gsJsLoader.with_module("/++resource++gs-profile-password-toggle-min-20130516.js", 
                           gs_login_toggle_init);
});
