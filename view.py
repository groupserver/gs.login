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

    def generateSeed( self ):
        return sha.new(str(time.time())).hexdigest()

    def passwordsEncrypted( self ):
        return not not self.context.acl_users.encrypt_passwords

    def processCredentials( self ):
        login = self.request.get('login', '')
        
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
            passhmac = self.request.get('password', '')
            seed = self.request.get('seed','')
            
            myhmac = hmac.new(password, login+password+seed, sha).hexdigest()

            state = passhmac == myhmac or False
        
        user = not not user
        o = password
        password = not not password

        return (state, user, password, o, passhmac)

Globals.InitializeClass( GSLoginView )
