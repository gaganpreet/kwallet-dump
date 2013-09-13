#!/usr/bin/env python

from distutils.core import setup

requirements = [pkg.split('=')[0] for pkg in open('requirements.txt').readlines()]

classifiers = ['Environment :: Console',
               'Programming Language :: Python :: 3',
               'Topic :: Desktop Environment :: K Desktop Environment (KDE)',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
               'Topic :: Security',
               'Topic :: Security :: Cryptography'
               ]

setup(name='kwallet-dump',
      version='1.0.0',
      description='Access KWallet files without KDE desktop',
      author='Gaganpreet Singh Arora',
      author_email='gaganpreet.arora@gmail.com',
      url='https://github.com/gaganpreet/kwallet-dump',
      scripts=['src/kwallet-dump.py',],
      keywords=['KWallet', 'KDE', 'kwl'],
      install_requires=requirements,
      long_description=open('README.md').read(),
      packages=['kwallet_dump'],
      package_dir = {'kwallet_dump': 'src/kwallet_dump'},
      classifiers=classifiers
    )
