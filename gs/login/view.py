# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, print_function, unicode_literals
from hashlib import sha1 as sha
from hmac import new as hmac_new
import sys
if (sys.version_info >= (3, )):
    from urllib.parse import splitquery, quote
else:
    from urllib import splitquery, quote  # lint:ok
from gs.content.base import SitePage
from .util import seedGenerator
from .loginaudit import LOGIN, BADPASSWORD, BADUSERID, LoginAuditor, \
    AnonLoginAuditor


class GSLoginView(SitePage):
    def __init__(self, context, request):
        super(GSLoginView, self).__init__(context, request)
        self.state = None

    def __call__(self):
        'Return the page with the correct MIME-type and status code.'
        response = self.request.response
        retval = super(GSLoginView, self).__call__()
        # --==mpj17=-- For some reason that I cannot fathom, despite 90
        # minutes of searching, I have to set the content type for the Login
        # page. Any ideas as to *why* can be sent to
        # <mpj17@onlinegroups.net>
        response.setHeader(b'Content-Type', b'text/html; charset=utf-8')
        # The reponse will be a previously set 30x Redirect, a 200 OK, or a
        #   403 Forbidden. A 401 is not returned because we are not doing
        #   basic or digest auth.
        if ((response.getStatus() == 200)
                and (not self.loggedInUserInfo.anonymous)):
            response.setStatus(403)
        return retval

    def passwordsEncrypted(self):
        return bool(self.context.acl_users.encrypt_passwords)

    @property
    def encryptionSeed(self):
        return seedGenerator()

    @property
    def logged_in_user_viewing_login(self):
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
        if not user:
            raise ValueError('There is no user.')
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
        cacheBuster = seedGenerator()
        url, query = splitquery(cameFrom)
        if not url:
            # Oddly, setting the default came_from to / does not work.
            url = '/'
        # Put a cache-buster at the end of the query
        if query:
            query = query + '&nc=%s' % cacheBuster
        else:
            query = 'nc=%s' % cacheBuster
        retval = '?'.join((url, query))

        assert retval
        return retval

    def password_matches(self, login, password):
        # For security reasons the password is rarely passed in
        #   en-clear. Instead the password is hashed with a seed (ph,
        #   below). To compare the password with the one on file
        #   (password, passed in) the system hashes the stored
        #   version, and then does a comparison.
        pw = self.request.get('password', '')
        seed = self.request.get('seed', '')
        ph = self.request.get('ph', '')
        if ph:
            passhmac = ph
        else:
            # blindly try the password, even if it's set to nothing
            msg = login + pw + seed
            passhmac = hmac_new(pw, msg, sha).hexdigest()
        msg = login + password + seed
        myhmac = hmac_new(password, msg, sha).hexdigest()

        retval = passhmac == myhmac
        assert type(retval) == bool
        return retval

    def processCredentials(self):
        '''Entry point for processing the Login page.'''
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
            else:  # Password does not match
                auditor.info(BADPASSWORD)
                self.state = (False, True, True)
        else:  # There is no user
            auditor = AnonLoginAuditor(self.context, self.siteInfo)
            auditor.info(BADUSERID, login)
            self.state = (False, False, False)
        assert(self.state)

    @property
    def supportMessage(self):
        msg = u'''Hello,

I saw a Permission Denied error when I visited\n    %s

I think I should be able to see this page because...

Thanks,
  %s\n  <%s%s>\n''' % \
            (self.request.get('came_from', ''), self.loggedInUserInfo.name,
             self.siteInfo.url, self.loggedInUserInfo.url)
        r = 'mailto:{0}?subject={1}&body={2}'
        retval = r.format(self.siteInfo.get_support_email(),
                          quote('Permission Denied'), quote(msg.encode('utf-8')))
        return retval
