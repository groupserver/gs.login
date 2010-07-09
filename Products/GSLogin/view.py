# coding=utf-8
'''GroupServer Login

'''
import Products.Five
from AccessControl.class_init import InitializeClass
try:
    # python 2.6
    from hashlib import md5
    from hashlib import sha1 as sha
except ImportError:
    import sha
    import md5
import hmac
import time
import urllib
import random

from Products.XWFCore.XWFUtils import getOption
from Products.CustomUserFolder.interfaces import IGSUserInfo
from util import getDivisionObjects, isGSUser, getCurrentUserDivision
from loginaudit import *

def seedGenerator( ):
    return sha.new(str(time.time())+str(random.random())).hexdigest()

class GSLoginView( Products.Five.BrowserView ):
    ''' View object for logging into a groupserver site.

    '''
    def __init__(self, context, request):
        assert request
        assert context
        self.context = context
        self.request = request
        self.siteInfo = Products.GSContent.interfaces.IGSSiteInfo( context )
        self.state = None

    def passwordsEncrypted( self ):
        return not not self.context.acl_users.encrypt_passwords

    def generateSeed( self ):
        return seedGenerator()

    @property
    def anonomous_viewing_page( self ):
        roles = self.request.AUTHENTICATED_USER.getRolesInContext(self.context)
        retval = 'Authenticated' not in roles
        
        assert type(retval) == bool
        return retval

    @property
    def logged_in_user_viewing_login( self ):
        url = self.request.URL0
        baseLoginURL = '%s/login.html' % self.siteInfo.url
        
        retval = (url == baseLoginURL and not(self.request.get('came_from', '')))
        assert type(retval) == bool
        return retval

    def processCredentials( self ):
        cache_buster = seedGenerator()

        login = self.request.get('login', '')
        
        if not login:
            return
        
        user = None
        userInfo = None
        password = None
        if login:
            if login.find('@') > 0:
                user = self.context.acl_users.get_userByEmail(login)
            if not user:
                user = self.context.acl_users.getUser(login)
            if user and isGSUser( user ): # check that we are actually a GSUser too
                password = user.get_password()
                if self.passwordsEncrypted():
                    # strip off the encoding declaration and the trailing '='
                    password = password.split('}')[-1][:-1]        
        state = False
        passhmac = ''
         # We always want the password, for logging
        if user:
            pw = self.request.get('password', '')
            seed = self.request.get('seed','')
            ph = self.request.get('ph', '')
            if ph:
                passhmac = ph
            else:
                # blindly try the password, even if it's set to nothing
                passhmac = hmac.new(pw, login+pw+seed, sha).hexdigest()            
            
            myhmac = hmac.new(password, login+password+seed, sha).hexdigest()
            
            state = passhmac == myhmac or False

        if state:
            # Password matches
            if self.passwordsEncrypted():
                storepass = '{SHA}%s=' % password
            else:
                storepass = password

            self.context.cookie_authentication.credentialsChanged(user, 
              str(user.getId()), storepass)
            
            came_from = self.request.get('came_from', '')
            persist = self.request.get('__ac_persistent', '')
            auditor = LoginAuditor(self.siteInfo, user)
            auditor.info(LOGIN, persist, 
                came_from and urllib.splitquery(came_from)[0] or self.siteInfo.url)

            redirect_to = ''
            if came_from:
                url, query = urllib.splitquery(came_from)
                if query:
                    query = query+'&nc=%s' % cache_buster
                else:
                    query = 'nc=%s' % cache_buster
                redirect_to = '?'.join((url, query))
            else:
                redirect_to = '/login_redirect?__ac_persistent=%s' % persist
                
            self.request.response.redirect(redirect_to)
        else:
            if user and not state:
                # Password does not match
                auditor = LoginAuditor(self.siteInfo, user)
                auditor.info(BADPASSWORD)
            else:
                # There is no user
                auditor = AnonLoginAuditor(self.context, self.siteInfo)
                auditor.info(BADUSERID, login)
                
        user = not not user
        password = not not password
        
        self.state = (state, user, password)

class GSLoginRedirect( Products.Five.BrowserView ):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.siteInfo = Products.GSContent.interfaces.IGSSiteInfo( context )

    def loginRedirect( self ):
        user = self.request.AUTHENTICATED_USER
        cache_buster = seedGenerator()
        if user:
            password = user.get_password()
            login = user.getId()
            userInfo = IGSUserInfo(user)
        else:
            return self.request.response.redirect('login.html?nc=%s' % cache_buster)

        # if we are logging into the public site, figure out where to go
        canonicalHost = ''
        if self.siteInfo.siteObj.getProperty('is_public', False):        
            current_division = getCurrentUserDivision(self.context, user)
            if current_division:
                canonicalHost = getOption(current_division, 'canonicalHost')

        seed = seedGenerator()
        passhash = hmac.new(password, login+password+seed, sha).hexdigest()
        
        base_uri = self.request.BASE0
        if canonicalHost:
            redirect_uri = 'http://%s' % canonicalHost
        else:
            redirect_uri = base_uri

        persist = self.request.get('__ac_persistent', '')

        if base_uri != redirect_uri:
            # NEVER set cookie credentials for the public site or we will be
            # trapped in redirect hell
            if self.siteInfo.siteObj.getProperty('is_public', False):            
                self.request.response.expireCookie( self.context.cookie_authentication.auth_cookie )
            redirect_to = ('%s/login.html?login=%s&ph=%s&seed=%s&__ac_persistent=%s' %
                            (redirect_uri, login, passhash, seed, persist))
        elif not password:
            redirect_to = '%s/password.html' % userInfo.url
        else:
            redirect_to = '%s?nc=%s' % (redirect_uri, cache_buster)
        
        self.request.response.redirect(redirect_to)

InitializeClass( GSLoginView )