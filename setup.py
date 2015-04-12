#!/usr/bin/env python 

from distutils.core import setup 

setup(name='exbackoff',
      version='1.1.1',
      description='Decorator-based exponential backoff',
      author='Roberto Aguilar', 
      author_email='roberto@zymbit.com',
      py_modules=['backoff'], 
      long_description=open('README.md').read(),
      url='http://github.com/rca/backoff',
      license='LICENSE.txt'
)
