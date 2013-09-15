#!/usr/bin/env python

import subprocess
from distutils.core import setup

requirements = [pkg.split('=')[0] for pkg in open('requirements.txt').readlines()]

description = 'Access KWallet files without KDE desktop'
try:
    subprocess.call(["pandoc", "README.md", "-f", "markdown", "-t", "rst", "-o", "README.rst"])
    long_description = open("README.rst").read()
except OSError:
    print("Pandoc not installed")
    long_description = description

classifiers = ['Environment :: Console',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 3',
               'Topic :: Desktop Environment :: K Desktop Environment (KDE)',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
               'Topic :: Security',
               'Topic :: Security :: Cryptography'
               ]

version = open('CHANGES.txt').readlines()[0][1:].strip()

setup(name='kwallet-dump',
      version=version,
      description=description,
      author='Gaganpreet Singh Arora',
      author_email='gaganpreet.arora@gmail.com',
      url='https://github.com/gaganpreet/kwallet-dump',
      scripts=['src/kwallet-dump.py',],
      keywords=['KWallet', 'KDE', 'kwl'],
      install_requires=requirements,
      long_description=long_description,
      packages=['kwallet_dump'],
      package_dir = {'kwallet_dump': 'src/kwallet_dump'},
      classifiers=classifiers
    )
