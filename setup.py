#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os

from setuptools import setup

version = None
with open('vks/__init__.py', 'r') as f:
    for line in f:
        m = re.match(r'^__version__\s*=\s*(["\'])([^"\']+)\1', line)
        if m:
            version = m.group(2)
            break

assert version is not None, \
    'Could not determine version number from vks/__init__.py'


def __read__(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='vks-bootstraper',
    version=version,
    url='https://github.com/vngcloud/vks-bootstraper',
    description='The CLI tool to boostrap the instances of VKS clusters.',
    long_description=__read__('README.md'),
    author='Cuong. Duong Manh',
    author_email='cuongdm3@vng.com.vn',
    include_package_data=True,
    license='Apache License 2.0',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
    install_requires=[
        "requests >= 2.31.0",
        "click >= 8.0.3",
    ],
    entry_points={
        'console_scripts': ['vks-bootstraper=vks.__main__:cli'],
    },
)
