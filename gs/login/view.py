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

    def processCredentials( self ):
        cache_buster = seedGenerator()

        login = self.request.get('login', '')
        
        if not login:
            return
        
        user = None
        password = None
        if login:
            if login.find('@') > 0:
                user = self.context.acl_users.get_userByEmail(login)
            if not user:
                user = self.context.acl_users.getUser(login)
            # Check that we are actually a GSUser too
            if user and isGSUser( user ): 
                password = user.get_password()
                if self.passwordsEncrypted():
                    # Strip off the encoding declaration and the 
                    #   trailing '='
                    password = password.split('}')[-1][:-1]
        
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        
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

InitializeClass( GSLoginView )

