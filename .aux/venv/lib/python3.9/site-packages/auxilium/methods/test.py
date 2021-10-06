# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.8, copyright Saturday, 02 October 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from os import getcwd
from os.path import basename
from logging import log, ERROR

from ..tools.const import ICONS
from ..tools.coverage_tools import coverage as _coverage, \
    cleanup as cleanup_coverage
from ..tools.git_tools import commit_git
from ..tools.quality_tools import quality as _quality
from ..tools.security_tools import security as _security
from ..tools.test_tools import test as _test, cleanup as cleanup_test


DID_NOT_COMMIT = 'test missing - did not commit'


def do(pkg=basename(getcwd()), commit=None, fail_fast=None,
       quality=None, security=None, coverage=None, cleanup=None,
       path=None, env=None, **kwargs):
    """run test process"""

    if cleanup:
        return cleanup_test(path) or cleanup_coverage(path)

    code = False
    if quality:
        code = code or _quality(pkg, venv=env)
    if security:
        code = code or _security(pkg, venv=env)
    if path:
        code = code or _test(path, fail_fast=fail_fast, venv=env)
        if coverage:
            code = code or _coverage(pkg, path, min_cov=coverage,
                                     fail_fast=fail_fast, venv=env)
        code = code or commit_git(commit)
    elif commit:
        log(ERROR, ICONS["error"] + DID_NOT_COMMIT)
        code = True
    return code
