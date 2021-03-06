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
import os.path
from logging import getLogger, StreamHandler, Formatter, basicConfig, DEBUG, INFO, WARNING

sys.path.append('.')
sys.path.append('..')
sys.path.append('test')

from regtest import RegressionTestCase, TestLoader, TextTestRunner
from regtest.regtest import LeftoverAssertValueError, MissingAssertValueError

TEST_DATA = 'test' + sep + 'data' if os.path.exists('test') else 'data'

_short_format = '%(asctime)s %(levelname)-5s %(message)s'
# _long_format = '%(asctime)s %(module)-14s %(levelname)-8s %(message)-120s'

logger = getLogger('regtest')
logger.setLevel(DEBUG)
stdout_handler = StreamHandler()
stdout_handler.setFormatter(Formatter(_short_format, '%Y%m%d %H%M%S'))
logger.addHandler(stdout_handler)

# basicConfig()


class MyTest(RegressionTestCase):
    def setUp(self):
        self.setFolderName(TEST_DATA)

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
            self.assertAlmostRegressiveEqual(i, key='myextra %d' % i)

    def tearDown(self):
        self.writeResults()
        self.logResults()


class MyTest1(RegressionTestCase):
    def setUp(self):
        self.setFolderName(TEST_DATA)
        self.setFileName('MyTest')
        self.readResults()

    def testtesting(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        self.assertRegressiveEqual(7)

    def testnew(self):
        self.assertAlmostRegressiveEqual(101.01)
        self.assertAlmostRegressiveEqual(101.01)
        self.assertRaises(MissingAssertValueError, self.assertAlmostRegressiveEqual, 101.01)

    def test123(self):
        for i in range(4):
            self.assertAlmostRegressiveEqual(i)

    def tearDown(self):
        if 'test123' in self._new_results:
            self.assertRaises(LeftoverAssertValueError, self.writeResults)
        self.logResults()


class MyTest2(RegressionTestCase):
    def setUp(self):
        self.bePrudent(False)
        self.setFolderName(TEST_DATA)
        self.setFileName('MyTest')
        self.readResults()

    def testtesting(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        self.assertRaises(AssertionError, self.assertRegressiveEqual, 6)

    def test123(self):
        for i in range(7):
            self.assertAlmostRegressiveEqual(i)

    def tearDown(self):
        self.logResults()


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
