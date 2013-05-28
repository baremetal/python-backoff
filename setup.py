#!/usr/bin/env python 

from distutils.core import setup 

setup(name='backoff', 
      version='1.0', 
      description='Decorator-based exponential backoff',
      author='Roberto Aguilar', 
      author_email='roberto@baremetal.io', 
      py_modules=['backoff'], 
      long_description=open('README.md').read(),
      url='http://github.com/rca/backoff',
      license='LICENSE.txt'
)
