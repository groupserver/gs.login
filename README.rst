============
``gs.login``
============
~~~~~~~~~~~~~~~~
The Sign In page
~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-04-02
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
 `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This product is responsible to showing the Login page for a
GroupServer site. The page can be shown in two ways:

#. The user explicitly visits ``login.html``, or
#. A Permission Denied error is generated.

In the latter case a login page is shown if the anonymous-user
generated the error, otherwise a Permission Denied error is
shown. The error has a link to the support email for the site, so
the user can easily contact support if they think that they saw
the error in error.

`A JavaScript library`_ by Paul Johnston is used to encrypt the
login. It is imported by the resource ``gs-login-20151106.js``.

Resources
=========

- Code repository: https://github.com/groupserver/gs.login
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _A JavaScript library: <http://pajhome.org.uk/crypt/md5/>`_

..  LocalWords:  ISiteHomeMain groupserver GroupListContent nz html
