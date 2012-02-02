#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from distutils.core import setup
import emailusernames

version = emailusernames.__version__

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print "You probably want to also tag the version now:"
    print "  git tag -a %s -m 'version %s'" % (version, version)
    print "  git push --tags"
    sys.exit()

setup(
    name='django-email-as-username',
    version=version,
    description='User authentication with email addresses instead of usernames.',
    author='Tom Christie',
    url='https://github.com/dabapps/django-email-as-username',
    packages=['emailusernames', ],
    install_requires=[],
    license='BSD',
)
