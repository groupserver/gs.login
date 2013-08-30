# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.login',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='login authentication',
      author='Richard Waid',
      author_email='richard@iopen.net',
      url='http://groupserver.org',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pytz',
          'zope.component',
          'zope.interface',
          'AccessControl',
          'gs.content.base',
          'gs.content.layout',
          'gs.database',
          'Products.CustomUserFolder',
          'Products.XWFCore',
          'Products.GSAuditTrail',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
