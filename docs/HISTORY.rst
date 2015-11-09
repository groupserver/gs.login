Changelog
=========

4.4.1 (2015-11-09)
------------------

* Updating the JavaScript to use strict mode

4.4.0 (2015-09-22)
------------------

* Using a capitol for ``Subject`` in the ``mailto``
* Naming the reStructuredText files as such
* Switching to GitHub_ as the primary repository 

.. _GitHub:
   https://github.com/groupserver/gs.login

4.3.4 (2014-05-13)
------------------

* Setting the ``403`` HTTP status-code
* Switching an ``assert`` to raising an error

4.3.2 (2014-03-24)
------------------

* Adding support for the ``zope.security.interfaces.Forbidden``
  exception

4.3.1 (2014-02-20)
------------------

* Switching to Unicode literals

4.3.0 (2014-01-22)
------------------

* Fixing the link to the FAQ, closing `Bug 4055`_

.. _Bug 4055: https://redmine.iopen.net/issues/4055

4.2.3 (2013-11-07)
------------------

* Switching to a Twitter Bootstrap alert

4.2.2 (2013-08-30)
------------------

* Updating the product metadata

4.2.1 (2013-06-06)
------------------

* Fixing the *Signed out* page

4.2.0 (2013-05-22)
------------------

* Using *Sign in* rather than *login*
* Adding the *Show password* toggle
* Adding the required-widgets JavaScript

4.1.0 (2013-04-02)
------------------

* Moving the JavaScript for login into its own file
* Adding the crypto JavaScript here from `Products.GSContent`_

.. _Products.GSContent:
   https://github.com/groupserver/Products.GSContent

4.0.3 (2012-08-01)
------------------

* Removing a redirect

4.0.2 (2012-06-22)
------------------

* Following the update to SQLAlchemy_

.. _SQLAlchemy: http://www.sqlalchemy.org/

4.0.1 (2012-06-06)
------------------

* Removing the *Easy login* viewlet from the site homepage

4.0.0 (2012-05-31)
------------------

* Removing *Sign up* from the *Login* page, closing `Issue 872`_
* Adding detail to the *Permission denied* page, closing `Issue
  646`_
* Refactoring the login code
* Dropping support for Python 2.4
* Removing the concept of *divisions*

.. _Issue 872: https://redmine.iopen.net/issues/872
.. _Issue 646: https://redmine.iopen.net/issues/646

3.0.0 (2011-07-26)
------------------

* Renaming the product ``gs.login`` from ``Products.GSLogin``

2.7.7 (2011-05-04)
------------------

* Showing login-events in the audit trail

2.7.6 (2011-02-03)
------------------

* Removing old page-templates

2.7.5 (2010-12-10)
------------------

* Using standard base-classes for the *Login* page
* Fixing so the ``hmac`` module is used
* Removing **old** pages

2.7.4 (2010-08-25)
------------------

* Forcing the password to be a string, rather than Unicode
* Updating the metadata

2.7.3 (2010-07-16)
------------------

* Unicode fix so logging works in both Zope 2.10 (Python 2.4) and
  (hopefully) Zope 2.13 (Python 2.6)


2.7.2 (2010-07-09)
------------------

* Fixing for ``urllib2`` in Python 2.6
* Fixing for MD5/SHA imports
* Fixing for deprecated code

2.7.1 (2010-04-01)
------------------

* Updating the metadata for the product

2.7.0 (2009-10-04)
------------------

* Turning the product into an egg

2.6.4 (2009-09-08)
------------------

* Removing the required-field check

2.6.3 (2009-08-21)
------------------

* Updating the metadata for the product

2.6.2 (2009-06-22)
------------------

* Hiding the *Utility* links on the *Login* page

2.6.1 (2009-03-05)
------------------

* Ensuring the pages output ``text/html`` rather than
  ``text/xml``

2.6.0 (2009-02-27)
------------------

* Improving the wording of the *Loin* page
* Adding audit trails

2.5.1 (2008-10-20)
------------------

* Removing unnecessary ``<html>`` elements

2.5.0 (2008-06-25)
------------------

* Redirecting users with no password to new-style *Set password*
  page

2.4.0 (2008-06-18)
------------------

* Adding a new version of the *Login* page
* Adding a cache-buster
* Removing the old registration code

2.3.1 (2008-05-05)
------------------

* Focusing the *Email address* field of the *Login* page when the
  page loads

2.3.0 (2008-04-17)
------------------

* Adding a new *Login* page, which shows something different to
  authenticated users

2.2.2 (2008-04-03)
------------------

* Fixing ``__ac_persistent``
* Improving the logging

2.2.1 (2008-03-25)
------------------

* Improving the logging

2.2.0 (2008-02-19)
------------------

* New *Reset password* page
* Improving the *Login* page help

2.1.1 (2008-01-15)
------------------

* Fixing the CSS class for the button

2.1.0 (2008-01-10)
------------------

* Adding a new *Login* page
* Removing all references to the profile-ID
* Adding popup help

2.0.0 (2007-12-20)
------------------

* Adding a *Registration* page
* Sifting many parts of Login from the ZMI to the filesystem
* Removing the profile-ID field from the form

1.2.0 (2007-11-26)
------------------

* Switching from Prototype to jQuery_

.. _jQuery: https://github.com/groupserver/gs.content.js.jquery.base

1.1.3 (2007-09-04)
------------------

* Fixing some client-specific login instructions, and
  site-skinning now works

1.1.2 (2007-08-04)
------------------

* Fixing some JavaScript

1.1.1 (2007-04-04)
------------------

* Clarifying that the user-identifier can be an email address or
  the profile-ID

1.1.0 (2007-02-22)
------------------

* Adding the ``__ac_persistent`` flag to any transferred login
  request

1.0.1 (2007-02-15)
------------------

* Fixing the JavaScript so it handled events not firing when
  enter is hit

1.0.0 (2007-02-11)
------------------

Initial version. Prior to the creation of this product login was
handled by the `Products.GroupServer`_ product, I think. The new
code included end-to-end HMAC encryption.

.. _Products.GroupServer:
   https://github.com/groupserver/Products.GroupServer

..  LocalWords:  Changelog reStructuredText
