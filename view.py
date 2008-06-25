# coding=utf-8
'''GroupServer Login

'''
import Products.Five, Globals
import sha
import md5
import hmac
import time
import urllib2
import random

from Products.XWFCore.XWFUtils import getOption
from Products.CustomUserFolder.interfaces import IGSUserInfo
from util import getDivisionObjects, isGSUser, getCurrentUserDivision

import logging
log = logging.getLogger('GSLogin')

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
            if self.passwordsEncrypted():
                storepass = '{SHA}%s=' % password
            else:
                storepass = password

            self.context.cookie_authentication.credentialsChanged(user, 
              str(user.getId()), storepass)
            
            userInfo = IGSUserInfo(user)
            m = 'Logging in %s (%s) to %s (%s)' %\
              (userInfo.name, userInfo.id, 
               self.siteInfo.name, self.siteInfo.id)
            log.info(m)

            came_from = self.request.get('came_from', '')
            redirect_to = ''
            if came_from:
                url, query = urllib2.splitquery(came_from)
                if query:
                    query = query+'&nc=%s' % cache_buster
                else:
                    query = 'nc=%s' % cache_buster
                redirect_to = '?'.join((url, query))
            else:
                persist = self.request.get('__ac_persistent', '')
                redirect_to = '/login_redirect?__ac_persistent=%s' % persist
                
            self.request.response.redirect(redirect_to)
        else:
            m = 'Not logging in user "%s" to %s (%s)' % (login, 
              self.siteInfo.name, self.siteInfo.id)
            log.info(m)
            if user and not state:
                userInfo = IGSUserInfo(user)
                m = 'User %s (%s) exists, so bad password' % \
                  (userInfo.name, userInfo.id)
            else:
                m = 'No such user "%s"' % login
            log.info(m)
                
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

        m = 'loginRedirect: Redirecting %s (%s) to <%s> on %s (%s)'%\
          (userInfo.name, userInfo.id, redirect_to, 
           self.siteInfo.name, self.siteInfo.id)
        log.info(m)
        m = 'loginRedirect: %s (%s) set Remember Me to "%s"'%\
          (userInfo.name, userInfo.id, persist)
        log.info(m)
        
        self.request.response.redirect(redirect_to)

Globals.InitializeClass( GSLoginView )
