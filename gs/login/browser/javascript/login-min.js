jQuery.noConflict();function loginSubmit(e){var d=null,c=null,g=null,b=null,a=null,f=null;
d=jQuery("#login-form");c=jQuery("#password").val();g=jQuery("#ep").val();if(g=="True"){c=b64_sha1(c)
}b=jQuery("#login").val();a=jQuery("#seed").val();f=hex_hmac_sha1(c,(b+c+a));jQuery("#ph").val(f);
jQuery("#password").val("")}function init_login(){jQuery("#login-form").submit(loginSubmit);
jQuery("#login").focus()}jQuery(window).load(function(){gsJsLoader.with_module("/++resource++crypto-20130402/sha1-min.js",init_login)
});