# coding=utf-8
'''The GroupServer Login page'''
from hashlib import sha1 as sha
from hmac import new as hmac_new
from urllib import splitquery, quote
from gs.content.base.page import SitePage
from util import isGSUser, seedGenerator
from loginaudit import *

class GSLoginView( SitePage ):
    def __init__(self, context, request):
        SitePage.__init__(self, context, request)
        self.state = None

    def passwordsEncrypted( self ):
        return bool(self.context.acl_users.encrypt_passwords)

    @property
    def encryptionSeed(self):
        return seedGenerator()

    @property
    def logged_in_user_viewing_login( self ):
        url = self.request.URL0
        baseLoginURL = '%s/login.html' % self.siteInfo.url
        
        retval = (url == baseLoginURL and 
                    not(self.request.get('came_from', '')))
        assert type(retval) == bool
        return retval

    def get_user_from_login(self, login):
        retval = None
        if login:
            aclUsers = self.context.acl_users
            if login.find('@') > 0:
                retval = aclUsers.get_userByEmail(login)
            if not retval:
                retval = aclUsers.getUser(login)
            # TODO: Nickname
        return retval

    def get_password_from_user(self, user):
        retval = None
        # Check that we are actually a GSUser too
        if user and isGSUser( user ): 
            retval = user.get_password()
            if self.passwordsEncrypted():
                # Strip off the encoding declaration and the trailing '='
                retval = retval.split('}')[-1][:-1]
        if isinstance(retval, unicode):
            retval = retval.encode('utf-8')
        return retval
    
    def store_password_cookie_for_user(self, user, password):
        if self.passwordsEncrypted():
            storepass = '{SHA}%s=' % password
        else:
            storepass = password
        cookieAuth = self.context.cookie_authentication
        uid = str(user.getId())
        cookieAuth.credentialsChanged(user, uid, storepass)
    
    def get_redirect(self):
        retval = ''
        cameFrom = self.request.get('came_from', '')
        if cameFrom:
            cacheBuster = seedGenerator()
            url, query = splitquery(cameFrom)
            if query:
                # Put a cache-buster at the end of the query
                query = query+'&nc=%s' % cacheBuster
            else:
                # Add a cache-buster
                query = 'nc=%s' % cacheBuster
            retval = '?'.join((url, query))
        else:
            persist = self.request.get('__ac_persistent', '')
            retval = '/login_redirect?__ac_persistent=%s' % persist
        assert retval
        return retval
    
    def password_matches(self, login, password):
        pw = self.request.get('password', '')
        seed = self.request.get('seed','')
        ph = self.request.get('ph', '')
        if ph:
            passhmac = ph
        else:
            # blindly try the password, even if it's set to nothing
            msg = login+pw+seed
            passhmac = hmac_new(pw, msg, sha).hexdigest()
        msg = login+password+seed
        myhmac = hmac_new(password, msg, sha).hexdigest()

        retval = passhmac == myhmac 
        assert type(retval) == bool
        return retval
        
    def processCredentials( self ):
        login = self.request.get('login', '')
        if not login:
            return
        user = self.get_user_from_login(login)
        if user:
            auditor = LoginAuditor(self.siteInfo, user)
            password = self.get_password_from_user(user)        
            if self.password_matches(login, password):
                self.store_password_cookie_for_user(user, password)
                uri = self.get_redirect()

                u = splitquery(uri)[0].replace('login_redirect', '')
                persist = self.request.get('__ac_persistent', '')
                auditor.info(LOGIN, persist, u)

                self.state = (True, True, True)
                self.request.response.redirect(uri)
            else: # Password does not match
                auditor.info(BADPASSWORD)
                self.state = (False, True, True)
        else: # There is no user
            auditor = AnonLoginAuditor(self.context, self.siteInfo)
            auditor.info(BADUSERID, login)
            self.state = (False, False, False)
        assert(self.state)

    @property
    def supportMessage(self):
        msg = u'Hello,\n\nI saw a Permission Denied error when I '\
            u'visited\n    %s\n\nI think I should be able to see this '\
            u'page because...' % self.request.get('came_from','')
        retval = 'mailto:%s?Subject=%s&body=%s'%\
            (self.siteInfo.get_support_email(), 
            quote('Permission Denied'), quote(msg.encode('utf-8')))
        return retval

