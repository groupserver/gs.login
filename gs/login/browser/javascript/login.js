jQuery.noConflict();

function loginSubmit(event) {
    var el = null, pw = null, encrypt = null, loginText = null, seed = null, new_passvalue = null;
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

function init_login() {
    jQuery('#login-form').submit(loginSubmit);
    jQuery('#login').focus();
}

jQuery(window).load( function() {
    gsJsLoader.with_module("/++resource++crypto/sha1.js", init_login);
});
