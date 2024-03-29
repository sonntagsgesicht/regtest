# -*- coding: utf-8 -*-

# regtest
# -------
# regression test enhancement for the Python unittest framework.
#
# Author:   sonntagsgesicht
# Version:  0.3.3, copyright Friday, 05 May 2023
# Website:  https://github.com/sonntagsgesicht/regtest
# License:  Apache License 2.0 (see LICENSE file)


import logging

from unittest import *  # noqa F401 F402

from .regtest import RegressionTestCase # noqa F401

logging.getLogger(__name__).addHandler(logging.NullHandler())

__doc__ = 'regression test enhancement for the Python unittest framework.'
__version__ = '0.3.3'
__dev_status__ = '4 - Beta'
__date__ = 'Friday, 05 May 2023'
__author__ = 'sonntagsgesicht'
__email__ = 'sonntagsgesicht@icloud.com'
__url__ = 'https://github.com/sonntagsgesicht/' + __name__
__license__ = 'Apache License 2.0'
__dependencies__ = ()
__dependency_links__ = ()
__data__ = ()
__scripts__ = ()
__theme__ = ''


# todo
#  fix tuple value from json are turned into a list, so compare load(dump())
