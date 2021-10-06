# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.8, copyright Saturday, 02 October 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


import logging
import sys

from datetime import datetime
from os import getcwd
from os.path import basename, join, exists

from auxilium import methods
from auxilium.tools.const import VERBOSITY_LEVELS, ICONS, DEMO_PATH
from auxilium.tools.system_tools import module, del_tree

Failure = Exception


def init_logging(verbosity=None, **kwargs):
    item = min(verbosity, len(VERBOSITY_LEVELS) - 1)
    verbosity, formatter = VERBOSITY_LEVELS[item]
    logging.basicConfig(level=verbosity, format=formatter)


def check_env(env=None, **kwargs):
    if env and not exists(env):
        msg = ICONS["warn"] + \
          'did not find a virtual environment at %s. ' % env
        logging.log(logging.WARN, msg)
        msg = ICONS[""] + \
            'consider creating one with ' \
            '`auxilium create --update` ' \
            'or use `auxilium -e command [options]`'
        logging.log(logging.WARN, msg)
        return True


def start_demo(demo=DEMO_PATH, verbosity=0, exit_status=0, env=None, **kwargs):
    logging.log(logging.INFO, ICONS["demo"] + 'relax, just starting a demo')
    del_tree(demo)
    v = '-' + 'v' * verbosity if verbosity else ''
    z = '-' + 'x' * exit_status if exit_status else ''
    e = '-e=' + env if env else ''
    cmd = (' %s %s %s create '
           '--name=%s '
           '--slogan="a demo by auxilium" '
           '--author=auxilium '
           '--email="sonntagsgesicht@icould.com" '
           '--url="https://github.com/sonntagsgesicht/auxilium"') % \
          (v, z, e, demo)
    return module('auxilium', cmd, level=logging.INFO)


def check_project_path(pkg=basename(getcwd()), path=getcwd(), **kwargs):
    full_path = join(path, pkg)
    if exists(full_path):
        # add project path to sys.path
        if path not in sys.path:
            sys.path.append(path)
        return

    msg = ICONS["warn"] + 'no maintainable project found at %s ' % path
    logging.log(logging.WARN, msg)
    msg = ICONS[""] + \
        'consider creating one with `auxilium create` ' \
        '(or did you mean `auxilium python`?)'
    logging.log(logging.WARN, msg)
    return True


def failure_exit(exit_status, command='unknown', **kwargs):
    msg = 'non-zero exit status (failure in `%s`)' % command
    logging.log(logging.ERROR, ICONS['error'] + msg)
    if exit_status > 2:
        raise Failure(msg)
    elif exit_status == 1:
        sys.exit(0)
    else:
        sys.exit(1)


def do(command=None, demo=None, verbosity=None, exit_status=None, env=None,
        **kwargs):
    # check demo
    if demo:
        if start_demo(demo, verbosity, exit_status, env):
            failure_exit(exit_status, command)
        sys.exit()

    # check virtual environment
    if command not in ('create',) and check_env(env):
        failure_exit(exit_status, command)

    # check project path
    if command not in ('create', 'python') and check_project_path():
        failure_exit(exit_status, command)

    # retriev command/method
    method = getattr(methods, str(command), None)

    # track execution timing
    start = datetime.now()

    # invoke command/method
    if method(**kwargs):
        failure_exit(exit_status, command)

    # track execution timing
    exec_time = (datetime.now() - start)

    logging.log(logging.INFO, ICONS['OK'] +
                'finished in %0.3fs' % exec_time.total_seconds())
    sys.exit()
