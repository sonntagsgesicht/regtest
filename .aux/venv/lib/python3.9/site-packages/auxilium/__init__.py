# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.9, copyright Saturday, 02 October 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


import logging

from .rst_tools import replacements_str, replacements_from_pkg, \
    replacements_from_cls, replacements  # noqa: F401

logging.getLogger(__name__).addHandler(logging.NullHandler())

__doc__ = 'Python project for an automated test and deploy toolkit.'
__version__ = '0.1.9'
__dev_status__ = '4 - Beta'
__date__ = 'Saturday, 02 October 2021'
__author__ = 'sonntagsgesicht'
__email__ = __author__ + '@icloud.com'
__url__ = 'https://github.com/' + __author__ + '/' + __name__
__license__ = 'Apache License 2.0'
__dependencies__ = 'pip', 'dulwich', 'flake8', 'bandit', 'coverage', \
                   'sphinx', 'sphinx-rtd-theme', 'sphinx-math-dollar', \
                   'twine', 'karma-sphinx-theme', 'sphinx-nameko-theme'
__dependency_links__ = ()
__data__ = ('data/pkg.zip',)
__scripts__ = ('auxilium/scripts/auxilium',)


# todo: picture link to github
# todo: update tutorial
