# -*- coding: utf-8 -*-

#  regtest
#  -------
#  regression test enhancement for the Python unittest framework
#
#  Author:  sonntagsgesicht <sonntagsgesicht@icloud.com>
#  Copyright: 2016, 2017
#  Website: https://github.com/sonntagsgesicht/regtest
#  License: APACHE Version 2 License (see LICENSE file)


import codecs
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='regtest',
    description='regression test enhancement for the Python unittest framework.',
    version='0.1',
    author='sonntagesicht',
    author_email='sonntagsgesicht@icloud.com',
    url='https://github.com/sonntagsgesicht/regtest',
    bugtrack_url='https://github.com/sonntagsgesicht/regtest/issues',
    license='Apache License 2.0',
    packages=['regtest'],
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Education',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Utilities',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
