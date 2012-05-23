# coding=utf-8
from hashlib import sha1 as sha
from hmac import new as hmac_new
from Products.XWFCore.XWFUtils import getOption
from gs.content.base.page import SitePage
from util import seedGenerator, getCurrentUserDivision

class GSLoginRedirect( SitePage ):
    def __init__(self, context, request):
        SitePage.__init__(self, context, request)

    def loginRedirect( self ):
        userInfo = self.loggedInUserInfo
        cache_buster = seedGenerator()
        if userInfo.anonymous:
            uri = 'login.html?nc=%s' % cache_buster
            retval = self.request.response.redirect(uri)
            return retval
        else:
            password = userInfo.user.get_password()
            if isinstance(password, unicode):
                password = password.encode('utf-8')
            login = userInfo.id

        # if we are logging into the public site, figure out where to go
        canonicalHost = ''
        if self.siteInfo.siteObj.getProperty('is_public', False):        
            current_division = getCurrentUserDivision(self.context, user)
            if current_division:
                canonicalHost = getOption(current_division, 'canonicalHost')

        seed = seedGenerator()
        passhash = hmac_new(password, login+password+seed, sha).hexdigest()
        
        base_uri = self.request.BASE0
        if canonicalHost:
            redirect_uri = 'http://%s' % canonicalHost
        else:
            redirect_uri = base_uri

        persist = self.request.get('__ac_persistent', '')

        if base_uri != redirect_uri:
            # NEVER set cookie credentials for the public site or we 
            # will be trapped in redirect hell
            isPublic = self.siteInfo.siteObj.getProperty('is_public', False)
            if isPublic:
                cookie = self.context.cookie_authentication.auth_cookie
                self.request.response.expireCookie( cookie )
            uri = '%s/login.html?login=%s&ph=%s&seed=%s&__ac_persistent=%s'%\
                    (redirect_uri, login, passhash, seed, persist)
        elif not password:
            uri = '%s/password.html' % userInfo.url
        else:
            uri = '%s?nc=%s' % (redirect_uri, cache_buster)
        
        self.request.response.redirect(uri)

