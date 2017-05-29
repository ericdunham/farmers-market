# -*- coding: utf-8 -*-

# stdlib imports
import os
# stdlib froms
from distutils.core import setup
# project froms
from market import version

cwd = os.path.abspath(os.path.dirname(__file__))

packages = ['market']

with open('README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    author="Eric Dunham",
    author_email="me@ericdunham.com",
    classifiers=(
        'Intended Audience :: Developers'
        'Intended Audience :: Hiring Managers'
        'Natural Language :: English'
        'License :: OSI Approved :: MIT License'
        'Programming Language :: Python'
        'Programming Language :: Python :: 3.5'
        'Programming Language :: Python :: 3.6'
    ),
    description="A basic shopping cart for the farmer's market",
    license='MIT License',
    long_description=readme,
    name="Farmer's Market",
    package_data={'': ['LICENSE']},
    package_dir={'market': 'market'},
    packages=packages,
    url="https://github.com/ericdunham/farmers-market",
    version=version.semantic
)
