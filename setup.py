#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'six>=1.10'
]

test_requirements = [
    'mock',
    'pytest',
]

setup_requirements = [
    'pytest-runner'
]


setup(
    name='babis',
    version='0.2.2',
    description="Decorator that pings URLs before and after executing the wrapped obj.",
    long_description=readme + '\n\n' + history,
    author="Giorgos Logiotatidis",
    author_email='seadog@sealabs.net',
    url='https://github.com/glogiotatidis/babis',
    packages=[
        'babis',
    ],
    package_dir={'babis':
                 'babis'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='babis',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
