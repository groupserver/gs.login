# coding=utf-8
from hashlib import sha1 as sha
from hmac import new as hmac_new
from Products.XWFCore.XWFUtils import getOption
from gs.content.base.page import SitePage
from util import seedGenerator

class GSLoginRedirect( SitePage ):
    def __init__(self, context, request):
        SitePage.__init__(self, context, request)

    def loginRedirect( self ):
        cache_buster = seedGenerator()
        if self.loggedInUserInfo.anonymous:
            uri = '/login.html?nc=%s' % cache_buster
            retval = self.request.response.redirect(uri)
            return retval

        canonicalHost = getOption(self.context, 'canonicalHost')
        base_uri = self.request.BASE0
        if canonicalHost:
            redirect_uri = 'http://%s' % canonicalHost
        else:
            redirect_uri = base_uri

        if base_uri != redirect_uri:
            # NEVER set cookie credentials or we will be trapped in 
            # redirect hell
            cookie = self.context.cookie_authentication.auth_cookie
            self.request.response.expireCookie( cookie )

            seed = seedGenerator()
            password = self.loggedInUserInfo.user.get_password()
            if isinstance(password, unicode):
                password = password.encode('utf-8')
            login = self.loggedInUserInfo.id
            msg = login+password+seed
            passhash = hmac_new(password, msg, sha).hexdigest()
            persist = self.request.get('__ac_persistent', '')
            uri = '/login.html?login=%s&ph=%s&seed=%s&__ac_persistent=%s'%\
                    (login, passhash, seed, persist)
        else:
            uri = '%s?nc=%s' % (redirect_uri, cache_buster)

        assert uri, 'There is no URI to redirect to.'        
        self.request.response.redirect(uri)

