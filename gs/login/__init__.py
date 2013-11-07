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
import AccessControl.AuthEncoding
from AccessControl.AuthEncoding import _schemes


def pw_validate(reference, attempt):
    """Validate the provided password string, which uses LDAP-style encoding
    notation.  Reference is the correct password, attempt is clear text
    password attempt."""

    for id, prefix, scheme in _schemes:
        lp = len(prefix)
        if reference[:lp] == prefix:
            # a significant tweak to handle our pre-encoded passwords
            if attempt[:lp] == prefix:
                return reference == attempt
            else:
                return scheme.validate(reference[lp:], attempt)
    # Assume cleartext.
    return (reference == attempt)

AccessControl.AuthEncoding.pw_validate = pw_validate
