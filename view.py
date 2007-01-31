'''GroupServer Login

'''
import Products.Five, Globals
import sha, hmac
import time

from Products.XWFCore.XWFUtils import getOption
from util import getDivisionObjects, isGSUser, getCurrentUserDivision

class GSLoginView( Products.Five.BrowserView ):
    ''' View object for logging into a groupserver site.

    '''
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.siteInfo = Products.GSContent.interfaces.IGSSiteInfo( context )
        self.state = None

    def generateSeed( self ):
        return sha.new(str(time.time())).hexdigest()

    def passwordsEncrypted( self ):
        return not not self.context.acl_users.encrypt_passwords

    def processCredentials( self ):
        login = self.request.get('login', '')
        
        if not login:
            return
        
        user = None
        password = None
        if login:
            user = self.context.acl_users.getUser(login)
            if user and isGSUser( user ): # check that we are actually a GSUser too
                password = user.get_password()
                if self.passwordsEncrypted():
                    # strip off the encoding declaration and the trailing '='
                    password = password.split('}')[-1][:-1]
        

        state = False
        passhmac = ''
        if user:
            passhmac = self.request.get('ph', '')
            seed = self.request.get('seed','')
            
            myhmac = hmac.new(password, login+password+seed, sha).hexdigest()
            
            state = passhmac == myhmac or False
        
        if state == True:
            if self.passwordsEncrypted():
                storepass = '{SHA}%s=' % password
            else:
                storepass = password
            
            self.context.cookie_authentication.credentialsChanged(user, login, storepass)
                        
            came_from = self.request.get('came_from', '')
            redirect_to = ''
            if came_from:
                redirect_to = came_from
            else:
                current_division = getCurrentUserDivision(self.context, user)
                if current_division:
                    canonicalHost = getOption(current_division, 'canonicalHost')
                else:
                    canonicalHost = ''
                
                seed = self.generateSeed()
                passhash = hmac.new(password, login+password+seed, sha).hexdigest()
                
                base_uri = self.request.BASE0
                if canonicalHost:
                    redirect_uri = 'http://%s' % canonicalHost
                else:
                    redirect_url = base_uri

                persist = self.request.get('__ac_persistent', '')
                
                if base_uri != redirect_uri:
                    redirect_to = ('%s/login.html?login=%s&ph=%s&seed=%s&__ac_persistent=%s' %
                                   (redirect_uri, login, passhash, seed, persist))
                elif not password:
                    # PPP: Need to be updated to pragmatic template
                    redirect_to = '%s/set_password.xml' % redirect_uri
                else:
                    redirect_to = '%s/loggedin.html' % redirect_uri
            
            self.request.response.redirect(redirect_to)                

        user = not not user
        password = not not password
        
        self.state = (state, user, password)

Globals.InitializeClass( GSLoginView )
