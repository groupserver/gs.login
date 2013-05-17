jQuery.noConflict();function gs_login_submit(e){var d=null,c=null,g=null,b=null,a=null,f=null;
d=jQuery("#login-form");c=jQuery("#password").val();g=jQuery("#ep").val();if(g=="True"){c=b64_sha1(c)
}b=jQuery("#login").val();a=jQuery("#seed").val();f=hex_hmac_sha1(c,(b+c+a));jQuery("#ph").val(f);
jQuery("#password").val("")}function gs_login_init(){jQuery("#login-form").submit(gs_login_submit)
}function gs_login_toggle_init(){var a=null;a=GSProfilePasswordToggle("#password","#gs-login-password-toggle-widget")
}jQuery(window).load(function(){jQuery("#login").focus();gsJsLoader.with_module("/++resource++crypto-20130402/sha1-min.js",gs_login_init);
gsJsLoader.with_module("/++resource++gs-profile-password-toggle-min-20130516.js",gs_login_toggle_init)
});