# -*- coding: utf-8 -*-

# regtest
# -------
# regression test enhancement for the Python unittest framework.
#
# Author:   sonntagsgesicht
# Version:  0.3.3, copyright Friday, 05 May 2023
# Website:  https://github.com/sonntagsgesicht/regtest
# License:  Apache License 2.0 (see LICENSE file)


from inspect import stack
from json import load, dump, loads, dumps
from logging import getLogger, NullHandler
from os.path import exists, sep, join
from os import makedirs
from unittest import TestCase
from gzip import open as zip

OPEN = zip
EXT = '.json.zip'

logger = getLogger(__name__)
logger.addHandler(NullHandler())


_ignore_ = object()


class NonContext(object):

    def __enter__(self):
        return

    def __exit__(self, *_):
        return


class MissingAssertValueError(KeyError):
    pass


class LeftoverAssertValueError(KeyError):
    pass


class RegressionTestCase(TestCase):

    folder = join('test', 'data')
    silent = False
    compression = True

    @property
    def alltestmethodnames(self):
        return tuple(m for m in dir(self) if m.startswith('test'))

    @property
    def rerun(self):
        return self._get_testmethod() in self._last_results

    def __init__(self, *args, **kwargs):
        super(RegressionTestCase, self).__init__(*args, **kwargs)
        self._last_results = dict()
        self._new_results = dict()

    def open(self, filename, mode="rb", *args, **kwargs):
        folderpath = join(self.folder, self.__class__.__name__)
        if not exists(folderpath) and 'w' in mode:
            makedirs(folderpath, exist_ok=True)

        filename += '.json.zip' if self.compression else '.json'
        filepath = join(folderpath, filename)
        if exists(filepath) or 'w' in mode:
            logger.info('  %s' % filepath.replace(self.folder + sep, ''))
            if self.compression:
                return zip(filepath, mode, *args, **kwargs)
            else:
                return open(filepath, mode, *args, **kwargs)
        return NonContext()

    def setUp(self):
        logger.info('')
        self.readResults()

    def tearDown(self):
        self.validateResults()
        self.writeResults()

    def validateResults(self):
        # validate all values have been used
        for key in self._new_results:
            leftover = self._last_results.get(key)
            if leftover:
                args = self.__class__.__name__, key, repr(leftover)
                msg = 'requested less values than available ' \
                      'for %s.%s: %s' % args
                if self.__class__.silent:
                    logger.warning(msg)
                else:
                    raise LeftoverAssertValueError(msg)

    def readResults(self):
        logger.info('read from %s' % (self.folder + sep))
        for test_method in self.alltestmethodnames:
            with self.open(test_method, 'rt') as file:
                if file:
                    self._last_results[test_method] = load(file)

    def writeResults(self):
        msg = 'write to %s' % (self.folder + sep)
        for test_method, data in list(self._new_results.items()):
            if test_method not in self._last_results:
                if msg:
                    logger.info(msg)
                    msg = ''
                with self.open(test_method, 'wt') as file:
                    dump(data, file, indent=2)

    def assertAlmostRegressiveEqual(
            self, new, places=7, msg=None, delta=None, key=()):
        # version 0.3.1, fixing tuple as list issue 'loads(dumps(tuple))=list'
        if isinstance(new, (tuple, set, list)):
            new = loads(dumps(list(new)))
        self._write_new(new, key)
        last = self._read_last(key)
        if last is _ignore_:
            return
        self._log_assert_call(last, new, places, msg, delta)
        try:
            return super(RegressionTestCase, self).assertAlmostEqual(
                last, new, places, msg, delta)
        except AssertionError as e:
            if self.silent:
                logger.warning(str(e))
            else:
                raise e

    def assertRegressiveEqual(self, new, msg=None, key=()):
        # version 0.3.1, fixing tuple as list issue 'loads(dumps(tuple))=list'
        if isinstance(new, (tuple, set, list)):
            new = loads(dumps(list(new)))
        self._write_new(new, key)
        last = self._read_last(key)
        if last is _ignore_:
            return
        self._log_assert_call(last, new, msg)
        try:
            return super(RegressionTestCase, self).assertEqual(last, new, msg)
        except AssertionError as e:
            if self.silent:
                logger.warning(str(e))
            else:
                raise e

    def _log_assert_call(self, *args, **kwargs):
        test_method = self.__class__.__name__ + '.' + \
                      RegressionTestCase._gather_method('test')
        assert_method = RegressionTestCase._gather_method('assert')
        pp = (lambda k, v: '%s: %s' % (str(k), repr(v)))
        kwargs = tuple(map(pp, kwargs))
        args = ', '.join(map(repr, args + kwargs))
        logger.debug('%-20s %s(%s)' % (test_method, assert_method, args))

    @staticmethod
    def _gather_method(name):
        m = None
        for line in reversed(stack()):
            if line[3].lower().startswith(name.lower()):
                m = line[3]
        if m is None:
            raise KeyError
        return m

    def _get_testmethod(self):
        return self._gather_method('test')

    def _read_last(self, key=()):
        testmethod = self._get_testmethod()
        key = key if key else testmethod
        if key in self._last_results:
            if self._last_results[key]:
                return self._last_results[key].pop(0)
            msg = 'requested more values than available for %s.%s.%s' % \
                  (self.__class__.__name__, testmethod, key)
            if self.__class__.silent:
                logger.warning(msg)
            else:
                raise MissingAssertValueError(msg)
        return _ignore_

    def _write_new(self, new, key=()):
        testmethod = self._get_testmethod()
        key = key if key else testmethod
        if key not in self._new_results:
            self._new_results[key] = list()
        self._new_results[key].append(new)
