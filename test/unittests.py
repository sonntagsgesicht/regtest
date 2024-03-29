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
from os import getcwd
from logging import getLogger, StreamHandler, Formatter, INFO

from regtest import RegressionTestCase, TestLoader, TextTestRunner
from regtest.regtest import LeftoverAssertValueError, MissingAssertValueError

logger = getLogger('regtest')
logger.setLevel(INFO)
stdout_handler = StreamHandler()
stdout_handler.setFormatter(
    Formatter('[%(levelname)-7s] %(message)s', '%Y%m%d %H%M%S'))
logger.addHandler(stdout_handler)


class AlmostRegressiveEqualTest(RegressionTestCase):

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
        values = 2 + 1e-8, 2 - 1e-8
        if self.rerun:
            values = reversed(values)
        for v in values:
            self.assertAlmostRegressiveEqual(v)

    def test_almost_regressive_equal_5(self):
        values = 2 + 1e-1, 2 - 1e-7
        self.assertAlmostRegressiveEqual(tuple(values))
        self.assertAlmostRegressiveEqual(set(values))
        self.assertAlmostRegressiveEqual(list(values))

class RegressiveEqualTest(RegressionTestCase):

    def test_regressive_equal_1(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        self.assertRegressiveEqual(7)

    def test_regressive_equal_2(self):
        for m in self.alltestmethodnames:
            self.assertRegressiveEqual(m)

    def test_regressive_equal_3(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        self.assertRegressiveEqual(7)

    def test_regressive_equal_4(self):
        values = 2 + 1e-1, 2 - 1e-7
        if self.rerun:
            for v in reversed(values):
                self.assertRaises(
                    AssertionError, self.assertRegressiveEqual, v)
        else:
            for v in values:
                self.assertRegressiveEqual(v)

    def test_regressive_equal_5(self):
        values = 2 + 1e-1, 2 - 1e-7
        self.assertRegressiveEqual(tuple(values))
        self.assertRegressiveEqual(set(values))
        self.assertRegressiveEqual(list(values))


class NoZipRegressiveEqualTest(RegressiveEqualTest):
    compression = False


class MissingTest(RegressionTestCase):

    def test_missing(self):
        self.assertAlmostRegressiveEqual(101.01)
        self.assertAlmostRegressiveEqual(101.01)
        if self.rerun:
            self.assertRaises(MissingAssertValueError,
                              self.assertAlmostRegressiveEqual,
                              101.01)


class AssertionErrorTest(RegressionTestCase):

    def test_assertion_error_equal(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        if self.rerun:
            self.assertRaises(AssertionError, self.assertRegressiveEqual, 6)
        else:
            self.assertRegressiveEqual(7)

    def test_assertion_error_almost_equal(self):
        self.assertAlmostRegressiveEqual(1)
        self.assertAlmostRegressiveEqual(1.1)
        if self.rerun:
            self.assertRaises(
                AssertionError, self.assertAlmostRegressiveEqual, 1.11)
        else:
            self.assertAlmostRegressiveEqual(1.01)


class LeftoverTest(RegressionTestCase):

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

    def test_key_error(self):
        self.assertRaises(KeyError, self._gather_method, 'xxx')


class SilentTest(RegressionTestCase):
    silent = True

    def test_leftover(self):
        cnt = 3 if self.rerun else 7
        for i in range(cnt):
            self.assertAlmostRegressiveEqual(i)

    def test_assertion_error_equal(self):
        self.assertRegressiveEqual(None)
        self.assertRegressiveEqual('not none')
        if self.rerun:
            self.assertRegressiveEqual(6)
        else:
            self.assertRegressiveEqual(7)

    def test_assertion_error_almost_equal(self):
        self.assertAlmostRegressiveEqual(1)
        self.assertAlmostRegressiveEqual(1.1)
        if self.rerun:
            self.assertAlmostRegressiveEqual(1.11)
        else:
            self.assertAlmostRegressiveEqual(1.01)

    def test_missing_almost_equal(self):
        self.assertAlmostRegressiveEqual(101.01)
        self.assertAlmostRegressiveEqual(101.01)
        if self.rerun:
            self.assertAlmostRegressiveEqual(101.01)

    def test_missing_equal(self):
        self.assertRegressiveEqual('A')
        self.assertAlmostRegressiveEqual(101.01)
        if self.rerun:
            self.assertRegressiveEqual('X')


if __name__ == "__main__":
    import sys

    start_time = datetime.now()

    print('')
    print('==================================================================')
    print('')
    print('run %s' % __file__)
    print('in %s' % getcwd())
    print('started  at %s' % str(start_time))
    print('')
    print('==================================================================')
    print('')

    suite = TestLoader().loadTestsFromModule(__import__("__main__"))
    testrunner = \
        TextTestRunner(stream=sys.stdout, descriptions=True, verbosity=2)
    testrunner.run(suite)

    suite = TestLoader().loadTestsFromModule(__import__("__main__"))
    testrunner = \
        TextTestRunner(stream=sys.stdout, descriptions=True, verbosity=2)
    testrunner.run(suite)

    print('')
    print('==================================================================')
    print('')
    print('ran %s' % __file__)
    print('in %s' % getcwd())
    print('started  at %s' % str(start_time))
    print('finished at %s' % str(datetime.now()))
    print('')
    print('==================================================================')
    print('')
