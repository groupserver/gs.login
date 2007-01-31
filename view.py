'''GroupServer Login

'''
import Products.Five, Globals
import sha, hmac
import time
import logging
logger = logging.getLogger('GSLogin')

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

    def getState( self ):
        return self.state

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
            passhmac = self.request.get('passhash', '')
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
                self.request.response.redirect('loggedin.html')
        
        user = not not user
        password = not not password
        
        self.state = (state, user, password)

Globals.InitializeClass( GSLoginView )
