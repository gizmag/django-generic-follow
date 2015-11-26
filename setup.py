#!/usr/bin/env python

from setuptools import setup, find_packages

REQUIRES = ['django']
try:
    import django
    if django.VERSION[:2] < (1, 7):
        REQUIRES.append("South")
except ImportError:
    pass

setup(
    name='django-generic-follow',
    version='0.4.2',
    description='Generic follow system for Django',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/django-generic-follow',
    packages=find_packages(exclude=['tests']),
    install_requires=REQUIRES
)
