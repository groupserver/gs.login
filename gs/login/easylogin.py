# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import
from gs.viewlet import SiteViewlet
from .util import seedGenerator


class EasyLogin(SiteViewlet):

    @property
    def show(self):
        retval = self.loggedInUser.anonymous
        assert type(retval) == bool
        return retval

    def passwordsEncrypted(self):
        return bool(self.context.acl_users.encrypt_passwords)

    @property
    def encryptionSeed(self):
        return seedGenerator()
