# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.8, copyright Saturday, 02 October 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from logging import log, INFO
from os import getcwd
from os.path import basename

from .const import ICONS
from .system_tools import module


def security(pkg=basename(getcwd()), venv=None):
    """evaluate security of source code"""
    log(INFO, ICONS["security"] + 'evaluate security of source code')
    return security_bandit(pkg, venv=venv)


def security_bandit(pkg=basename(getcwd()), venv=None):
    """run `bandit` on source code """
    return module('bandit', '-r -q %s' % pkg, venv=venv)
