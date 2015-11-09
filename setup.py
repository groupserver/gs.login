# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015 
# OnlineGroups.net and Contributors.
#
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
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

name = 'gs.login'
version = get_version()

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(
    name=name,
    version=version,
    description="The Sign in page for GroupServer",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Natural Language :: French",
        "Natural Language :: German",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='groupserver, message, email, post, plain text, ',
    author='Richard Waid',
    author_email='richard@onlinegroups.net',
    maintainer='Michael JasonSmith',
    maintainer_email='mpj17@onlinegroups.net',
    url='https://github.com/groupserver/{0}/'.format(name),
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['.'.join(name.split('.')[:i])
                        for i in range(1, len(name.split('.')))],
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
    """,)
