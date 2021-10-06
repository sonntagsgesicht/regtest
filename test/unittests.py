# -*- coding: utf-8 -*-

# regtest
# -------
# regression test enhancement for the Python unittest framework.
#
# Author:   sonntagsgesicht
# Version:  0.1, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/regtest
# License:  Apache License 2.0 (see LICENSE file)


import sys

from datetime import datetime
from os import getcwd, sep
from os.path import split
from logging import getLogger, StreamHandler, Formatter, basicConfig, DEBUG, INFO, WARNING

from regtest import RegressionTestCase, TestLoader, TextTestRunner
from regtest.regtest import LeftoverAssertValueError, MissingAssertValueError

_short_format = '%(asctime)s %(levelname)-5s %(message)s'
# _long_format = '%(asctime)s %(module)-14s %(levelname)-8s %(message)-120s'

logger = getLogger('regtest')
logger.setLevel(DEBUG)
stdout_handler = StreamHandler()
stdout_handler.setFormatter(Formatter(_short_format, '%Y%m%d %H%M%S'))
logger.addHandler(stdout_handler)

# basicConfig()

FOLDER = split(__file__)[0] + sep + 'DATA'


class MyTest(RegressionTestCase):

    data_folder = FOLDER

    def testtesting(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        self.assertRegressiveEqual(7)

    def testnew(self):
        self.assertAlmostRegressiveEqual(101.01)
        self.assertAlmostRegressiveEqual(101.01)

    def test123(self):
        for i in range(5):
            self.assertAlmostRegressiveEqual(i)

    def test123r(self):
        for i in range(5):
            self.assertAlmostRegressiveEqual(i, key='myextra')
            self.assertAlmostRegressiveEqual(i, key='myextra')


class MyTest1(RegressionTestCase):

    data_folder = FOLDER

    def testtesting(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        self.assertRegressiveEqual(7)

    def testnew(self):
        new = 'testnew' not in self._last_results
        self.assertAlmostRegressiveEqual(101.01)
        self.assertAlmostRegressiveEqual(101.01)
        if not new:
            self.assertRaises(MissingAssertValueError,
                              self.assertAlmostRegressiveEqual, 101.01)

    def test123(self):
        for i in range(4):
            self.assertAlmostRegressiveEqual(i)


class MyTest2(RegressionTestCase):
    data_folder = FOLDER
    fail_fast = False

    def testtesting(self):
        new = 'testtesting' not in self._last_results
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        if new:
            self.assertRegressiveEqual(7)
        else:
            self.assertRaises(AssertionError, self.assertRegressiveEqual, 6)

    def test123(self):
        for i in range(7):
            self.assertAlmostRegressiveEqual(i)


if __name__ == "__main__":
    import sys

    start_time = datetime.now()

    print('')
    print('======================================================================')
    print('')
    print('run %s' % __file__)
    print('in %s' % getcwd())
    print('started  at %s' % str(start_time))
    print('')
    print('----------------------------------------------------------------------')
    print('')

    suite = TestLoader().loadTestsFromModule(__import__("__main__"))
    testrunner = TextTestRunner(stream=sys.stdout, descriptions=2, verbosity=2)
    testrunner.run(suite)

    print('')
    print('======================================================================')
    print('')
    print('ran %s' % __file__)
    print('in %s' % getcwd())
    print('started  at %s' % str(start_time))
    print('finished at %s' % str(datetime.now()))
    print('')
    print('----------------------------------------------------------------------')
    print('')
