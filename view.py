'''GroupServer Login

'''
import Products.Five, Globals
import sha, hmac
import time

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
            if user:
                password = user.get_password()
                if self.passwordsEncrypted():
                    # strip off the encoding declaration and the trailing '='
                    password = password.split('}')[-1][:-1]
        
        state = False
        passhmac = ''
        if user and password:
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
            if came_from:
                self.request.response.redirect(came_from)
            else:
                seed = self.generateSeed()
                passhash = hmac.new(password, login+password+seed, sha).hexdigest()
                base_uri = self.request.BASE0
                redirect_uri = 'http://groupserver2:8080'
                persist = self.request.get('__ac_persistent', '')
                if base_uri != redirect_uri:
                    self.request.response.redirect(
                      '%s/login.html?login=%s&ph=%s&seed=%s&__ac_persistent=%s' %
                      (redirect_uri, login, passhash, seed, persist))
                else:
                    self.request.response.redirect('%s/loggedin.html' % redirect_uri)
                
        user = not not user
        password = not not password
        
        self.state = (state, user, password)

Globals.InitializeClass( GSLoginView )
