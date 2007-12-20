'''GroupServer Login

'''
import Products.Five, Globals
import sha, hmac
import time

from Products.XWFCore.XWFUtils import getOption
from util import getDivisionObjects, isGSUser, getCurrentUserDivision

def seedGenerator( ):
    return sha.new(str(time.time())).hexdigest()

class GSLoginView( Products.Five.BrowserView ):
    ''' View object for logging into a groupserver site.

    '''
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.siteInfo = Products.GSContent.interfaces.IGSSiteInfo( context )
        self.state = None

    def passwordsEncrypted( self ):
        return not not self.context.acl_users.encrypt_passwords

    def generateSeed( self ):
        return seedGenerator()

    def processCredentials( self ):
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
            if user and isGSUser( user ): # check that we are actually a GSUser too
                password = user.get_password()
                if self.passwordsEncrypted():
                    # strip off the encoding declaration and the trailing '='
                    password = password.split('}')[-1][:-1]        
        state = False
        passhmac = ''
        if user:
            seed = self.request.get('seed','')
            pw = self.request.get('password', '')
            ph = self.request.get('ph', '')
            if ph:
                passhmac = ph
            else:
                # blindly try the password, even if it's set to nothing
                passhmac = hmac.new(pw, login+pw+seed, sha).hexdigest()            
            
            myhmac = hmac.new(password, login+password+seed, sha).hexdigest()
            
            state = passhmac == myhmac or False
        
        if state == True:
            if self.passwordsEncrypted():
                storepass = '{SHA}%s=' % password
            else:
                storepass = password

            self.context.cookie_authentication.credentialsChanged(user, str(user.getId()), storepass)
            
            came_from = self.request.get('came_from', '')
            redirect_to = ''
            if came_from:
                redirect_to = came_from
            else:
                persist = self.request.get('__ac_persistent', '')
                redirect_to = '/login_redirect?__ac_persistent=%s' % persist
                
            self.request.response.redirect(redirect_to)                

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
        if user:
            password = user.get_password()
            login = user.getId()
        else:
            return self.request.response.redirect('login.html')

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
            # PPP: Need to be updated to pragmatic template
            redirect_to = '%s/set_password.xml' % redirect_uri
        else:
            redirect_to = '%s/' % redirect_uri

                        

        
        self.request.response.redirect(redirect_to)

Globals.InitializeClass( GSLoginView )
