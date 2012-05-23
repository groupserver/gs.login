# coding=utf-8
'''GroupServer Login'''
try:
    # Python 2.6
    from hashlib import sha1 as sha
except ImportError:
    # --=mpj17=-- Question: Do we need to support Python 2.4?
    # Python 2.4
    import sha
import hmac, urllib
from App.class_init import InitializeClass
from gs.content.base.page import SitePage
from util import isGSUser, seedGenerator
from loginaudit import *

class GSLoginView( SitePage ):
    ''' View object for logging into a groupserver site. '''
    def __init__(self, context, request):
        SitePage.__init__(self, context, request)
        self.state = None

    def passwordsEncrypted( self ):
        return not not self.context.acl_users.encrypt_passwords

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
                # Strip off the encoding declaration and the 
                #   trailing '='
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
    
    def processCredentials( self ):
        login = self.request.get('login', '')
        if not login:
            return
        
        cache_buster = seedGenerator()
        user = self.get_user_from_login(login)
        password = self.get_password_from_user(user)        
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
                msg = login+pw+seed
                passhmac = hmac.new(pw, msg, sha).hexdigest()
            msg = login+password+seed
            myhmac = hmac.new(password, msg, sha).hexdigest()
            state = passhmac == myhmac
            
            if state:
                # Password matches
                self.store_password_cookie_for_user(user, password)
                came_from = self.request.get('came_from', '')
                persist = self.request.get('__ac_persistent', '')
                auditor = LoginAuditor(self.siteInfo, user)
                u = ((came_from and urllib.splitquery(came_from)[0]) 
                        or self.siteInfo.url)
                auditor.info(LOGIN, persist, u)

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
            else: # not state
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

InitializeClass( GSLoginView )

