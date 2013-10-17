#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup


# monkey patch os.link to force using symlinks
import os
del os.link

setup(name='PyPromise',\
    version='1.1.2',\
    description='Python Promise implementation',\
    license='New BSD License',\
    author='Michał Bachowski',\
    author_email='michal@bachowski.pl',\
    package_dir={'': 'src'},\
    py_modules=['promise'])
