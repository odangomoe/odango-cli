#!/usr/bin/env python

from distutils.core import setup

setup(
    license="MIT",
    name='odango',
    version='1.0',
    description='A CLI tool for odango.moe',
    author='eater',
    author_email='odango@eater.me',
    url='https://odango.moe',
    packages=['odango'],
    install_requires=['colorama', 'requests'],
    entry_points={
         'console_scripts': ['odango=odango.__main__:main'],
    }
)
