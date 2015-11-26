#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-generic-follow',
    version='0.4.0',
    description='Generic follow system for Django',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/django-generic-follow',
    packages=find_packages(exclude=['tests']),
    install_requires=['django>=1.8']
)
