# -*- coding: utf-8 -*-

# regtest
# -------
# regression test enhancement for the Python unittest framework.
#
# Author:   sonntagsgesicht
# Version:  0.1, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/regtest
# License:  Apache License 2.0 (see LICENSE file)
import os.path
import sys

from datetime import datetime
from os import getcwd, sep
from os.path import split
from logging import getLogger, StreamHandler, Formatter, DEBUG


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

FOLDER = split(__file__)[0] + sep + 'REGTEST_DATA'


class AlmostRegressiveEqualTest(RegressionTestCase):

    data_folder = FOLDER

    def test_almost_regressive_equal_1(self):
        self.assertAlmostRegressiveEqual(101.01)
        self.assertAlmostRegressiveEqual(101.01)

    def test_almost_regressive_equal_2(self):
        for i in range(5):
            self.assertAlmostRegressiveEqual(i)

    def test_almost_regressive_equal_3(self):
        for i in range(5):
            self.assertAlmostRegressiveEqual(i, key='myextra')
            self.assertAlmostRegressiveEqual(i, key='myextra')

    def test_almost_regressive_equal_4(self):
        values = 2+1e-8, 2-1e-8
        if self.rerun:
            values = reversed(values)
        for v in values:
            self.assertAlmostRegressiveEqual(v)


class RegressiveEqualTest1(RegressionTestCase):

    data_folder = FOLDER

    def test_regressive_equal_1(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        self.assertRegressiveEqual(7)

    def test_regressive_equal_2(self):
        for f in self.filenames:
            self.assertRegressiveEqual(f)

    def test_regressive_equal_3(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        self.assertRegressiveEqual(7)

    def test_regressive_equal_4(self):
        values = 2+1e-1, 2-1e-7
        if self.rerun:
            for v in reversed(values):
                self.assertRaises(AssertionError, self.assertRegressiveEqual, v)
        else:
            for v in values:
                self.assertRegressiveEqual(v)


class MissingTest(RegressionTestCase):

    data_folder = FOLDER

    def test_missing(self):
        self.assertAlmostRegressiveEqual(101.01)
        self.assertAlmostRegressiveEqual(101.01)
        if self.rerun:
            self.assertRaises(MissingAssertValueError,
                              self.assertAlmostRegressiveEqual, 101.01)


class AssertionErrorTest(RegressionTestCase):
    data_folder = FOLDER

    def test_assertion_error(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        if self.rerun:
            self.assertRaises(AssertionError, self.assertRegressiveEqual, 6)
        else:
            self.assertRegressiveEqual(7)


class LeftoverTest(RegressionTestCase):
    data_folder = FOLDER

    def test_leftover(self):
        cnt = 3 if self.rerun else 7
        for i in range(cnt):
            self.assertAlmostRegressiveEqual(i)

    def tearDown(self):
        if 'test_leftover' in self._last_results:
            self.assertRaises(LeftoverAssertValueError, self.validateResults)
        else:
            self.validateResults()
        self.writeResults()


class GatherMethodTest(RegressionTestCase):
    data_folder = FOLDER

    def test_key_error(self):
        self.assertRaises(KeyError, self._gather_method, 'xxx')


class ClearResultsTest(RegressionTestCase):
    data_folder = FOLDER

    def test_this(self):
        self.assertRegressiveEqual('123')
        self.assertRegressiveEqual(123)

    def tearDown(self):
        self.validateResults()
        self.writeResults()
        self.clearResults()
        for f in self.filenames:
            self.assertFalse(os.path.exists(f))


class SilentTest(RegressionTestCase):
    data_folder = FOLDER
    silent = True

    def test_leftover(self):
        cnt = 3 if self.rerun else 7
        for i in range(cnt):
            self.assertAlmostRegressiveEqual(i)

    def test_assertion_error(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        if self.rerun:
            self.assertRegressiveEqual(6)
        else:
            self.assertRegressiveEqual(7)

    def test_missing(self):
        self.assertAlmostRegressiveEqual(101.01)
        self.assertAlmostRegressiveEqual(101.01)
        if self.rerun:
            self.assertAlmostRegressiveEqual(101.01)


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
