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


def quality(pkg=basename(getcwd()), venv=None):
    """evaluate quality of source code"""
    log(INFO, ICONS["quality"] + 'evaluate quality of source code')
    return quality_flake8(pkg, venv)


def quality_pylint(pkg=basename(getcwd()), venv=None):
    """evaluate quality of source code with pylint"""
    return module('pylint', pkg, venv=venv)


def quality_flake8(pkg=basename(getcwd()), venv=None):
    """evaluate quality of source code with flake8"""
    return module('flake8', '%s' % pkg, venv=venv)


def quality_pep8(pkg=basename(getcwd()), venv=None):
    """evaluate quality of source code with pep8/pep257"""
    exit_status = module('pycodestyle', pkg, venv=venv)
    return exit_status or module('pydocstyle', pkg, venv=venv)
