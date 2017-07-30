from datetime import datetime
from os import getcwd
from logging import getLogger, DEBUG, INFO, WARNING
from regtest import RegressionTestCase, TestLoader, TextTestRunner
from regtest.regtest import LeftoverAssertValueError, MissingAssertValueError

getLogger('regtest').setLevel(DEBUG)


class MyTest(RegressionTestCase):

    def setUp(self):
        self.setFolderName('data')

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

    def tearDown(self):
        self.writeResults()
        self.logResults()


class MyTest1(RegressionTestCase):

    def setUp(self):
        self.setFolderName('data')
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
        self.setFolderName('data')
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
    testrunner = TextTestRunner(stream=sys.stdout , descriptions=2, verbosity=2)
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