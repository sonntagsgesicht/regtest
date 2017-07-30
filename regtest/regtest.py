from inspect import stack
from json import load, dump
from logging import getLogger, StreamHandler, Formatter
from os.path import exists, sep
from os import remove
from unittest import TestCase

_short_format = '%(asctime)s %(levelname)-5s %(message)s'
_long_format = '%(asctime)s %(module)-14s %(levelname)-8s %(message)-120s'
logger = getLogger('regtest')
stdout_handler = StreamHandler()
stdout_handler.setFormatter(Formatter(_short_format, '%Y%m%d %H%M%S'))
logger.addHandler(stdout_handler)


class _ignore_(object):
    pass


class MissingAssertValueError(KeyError):
    pass


class LeftoverAssertValueError(KeyError):
    pass


class RegressionTestCase(TestCase):

    @property
    def filename(self):
        return self._foldername + sep + self._filename

    def __init__(self, *args, **kwargs):
        super(RegressionTestCase, self).__init__(*args, **kwargs)
        self._last_results = dict()
        self._new_results = dict()
        self._foldername = '.'
        self._filename = self.__class__.__name__ + '.json'
        self._prudent = True

    def bePrudent(self, be=True):
        self._prudent = be

    def clearResults(self):
        if exists(self.filename):
            remove(self.filename)

    def setUp(self):
        self.readResults()

    def tearDown(self):
        self.writeResults()

    def setFileName(self, filename):
        self._filename = filename + '.json'

    def setFolderName(self, foldername):
        self._foldername = foldername

    def readResults(self):
        logger.debug('read from %s' % self.filename)
        if exists(self.filename):
            with open(self.filename) as data_file:
                self._last_results = load(data_file)

    def writeResults(self):
        logger.debug('write to %s' % self.filename)

        # validate all values have been used
        for key in self._new_results:
            leftover = self._last_results.get(key)
            if leftover:
                args = self.__class__.__name__, key, repr(leftover)
                msg = 'requested less values than available for %s.%s: %s' % args
                if self._prudent:
                    raise LeftoverAssertValueError(msg)
                else:
                    logger.warning(msg)
                    self._last_results.pop(key)

        last_results = dict()
        if exists(self.filename):
            with open(self.filename) as data_file:
                last_results = load(data_file)

        for k, v in self._new_results.items():
            if k not in self._last_results:
                last_results[k] = v

        with open(self.filename, 'w') as data_file:
            dump(last_results, data_file)

    def logResults(self, filename=None, foldername=None):
        if filename is None:
            filename = self.__class__.__name__ + '.log'
        if foldername is None:
            foldername = self._foldername
        filename = foldername + sep + filename
        assert filename is not self.filename
        logger.debug('log to %s' % filename)

        last_results = dict()
        if exists(filename):
            with open(filename) as data_file:
                last_results = load(data_file)

        for k, v in self._new_results.items():
            if k not in last_results:
                last_results[k] = v

        with open(filename, 'w') as data_file:
            dump(last_results, data_file)

    def assertAlmostRegressiveEqual(self, new, places=7, msg=None, delta=None):
        self._write_new(new)
        last = self._read_last()
        if last is not _ignore_:
            self._log_assert_call(last, new, places, msg, delta)
            return super(RegressionTestCase, self).assertAlmostEqual(last, new, places, msg, delta)

    def assertRegressiveEqual(self, new, msg=None):
        self._write_new(new)
        last = self._read_last()
        if last is not _ignore_:
            self._log_assert_call(last, new, msg)
            return super(RegressionTestCase, self).assertEqual(last, new, msg)

    def _log_assert_call(self, *args, **kwargs):
        test_method = self.__class__.__name__ + '.' + RegressionTestCase._gather_method('test')
        assert_method = RegressionTestCase._gather_method('assert')
        pp = lambda k, v: '%s: %s' %(str(k), repr(v))
        kwargs = tuple(map(pp, kwargs))
        args = ', '.join(map(repr, args+kwargs))
        logger.info('%s %s(%s)' % (test_method.ljust(20), assert_method, args))

    @staticmethod
    def _gather_method(name):
        m = None
        for line in reversed(stack()):
            if line[3].lower().startswith(name.lower()):
                m = line[3]
        if m is None:
            raise KeyError
        return m

    def _get_key(self):
        return self._gather_method('test')

    def _read_last(self):
        key = self._get_key()
        if key in self._last_results:
            if self._last_results[key]:
                last = self._last_results[key].pop(0)
                if isinstance(last, unicode):
                    last = last.encode('ascii', 'ignore')
                return last
            else:
                msg = 'requested more values than available for %s.%s' % (self.__class__.__name__, key)
                if self._prudent:
                    raise MissingAssertValueError(msg)
                else:
                    logger.warning(msg)
                    self._last_results.pop(key)
        return _ignore_

    def _write_new(self, new):
        key = self._get_key()
        if key not in self._new_results:
            self._new_results[key] = list()
        self._new_results[key].append(new)
