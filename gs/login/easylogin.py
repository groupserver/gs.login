# coding=utf-8
from gs.viewlet.viewlet import SiteViewlet
from util import seedGenerator

class EasyLogin(SiteViewlet):

    @property
    def show(self):
        retval = self.loggedInUser.anonymous
        assert type(retval) == bool
        return retval

    def passwordsEncrypted( self ):
        return bool(self.context.acl_users.encrypt_passwords)

    @property
    def encryptionSeed(self):
        return seedGenerator()

