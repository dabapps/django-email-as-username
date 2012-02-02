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


def get_packages(root):
    """
    Return root package and all sub-packages.
    """
    return [x[0] for x in os.walk(root)
        if os.path.exists(os.path.join(x[0], '__init__.py'))]


def get_package_data(root):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(x[0].lstrip(root + os.sep), x[2]) for x in os.walk(root)
            if not os.path.exists(os.path.join(x[0], '__init__.py'))]

    file_list = []
    for base, files in walk:
        file_list.extend([os.path.join(base, file) for file in files])
    return {root: file_list}


setup(
    name='django-email-as-username',
    version=version,
    description='User authentication with email addresses instead of usernames.',
    author='Tom Christie',
    url='https://github.com/dabapps/django-email-as-username',
    packages=get_packages('emailusernames'),
    package_data=get_package_data('emailusernames'),
    license='BSD',
)
