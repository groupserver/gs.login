# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
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
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.login',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='login authentication',
      author='Richard Waid',
      author_email='richard@onlinegroups.net',
      maintainer='Michael JasonSmith',
      maintainer_email='mpj17@onlinegroups.net',
      url='https://source.iopen.net/groupserver/gs.login/',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pytz',
          'zope.browserpage',
          'zope.browserresource',
          'zope.component',
          'zope.interface',
          'zope.tal',
          'zope.tales',
          'AccessControl',
          'gs.content.base',
          'gs.content.layout',
          'gs.core',
          'gs.database',
          'Products.CustomUserFolder',
          'Products.XWFCore',
          'Products.GSAuditTrail',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
