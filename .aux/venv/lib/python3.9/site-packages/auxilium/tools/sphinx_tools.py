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
from os import getcwd, name as os_name
from os.path import exists, basename, normpath, join
from shutil import rmtree

from .const import ICONS
from .system_tools import shell

PATH = normpath("doc/sphinx/")
API_PATH = join(PATH, "api")
BUILD_PATH = join(PATH, "_build")
HTML_PATH = join(BUILD_PATH, "html")
LATEX_PATH = join(BUILD_PATH, "latex")
INDEX_FILE = join(HTML_PATH, "intro.html")


def api(pkg=basename(getcwd()), venv=None):
    """add api entries to `sphinx` docs"""
    log(INFO, ICONS["commit"] + 'run sphinx apidoc scripts')
    if exists(API_PATH):
        rmtree(API_PATH)
    cmd = "sphinx-apidoc -o %s -f -E %s" % (API_PATH, pkg)
    return shell(cmd, venv=venv)


def html(fail_fast=False, venv=None):
    """build html documentation (using `sphinx`)"""
    log(INFO, ICONS["html"] +
        'run sphinx html scripts (only on new or modified files)')
    ff = '' if fail_fast else " --keep-going"
    cmd = "sphinx-build -W %s -b html %s %s" % (ff, PATH, HTML_PATH)
    return shell(cmd, venv=venv)


def latexpdf(fail_fast=False, venv=None):
    """build pdf documentation (using `sphinx` and `LaTeX`)"""
    log(INFO, ICONS["latexpdf"] +
        'run sphinx latexpdf scripts (only on new or modified files)')
    ff = '' if fail_fast else " --keep-going"
    cmd = "sphinx-build -W %s -b latexpdf %s %s" % (ff, PATH, LATEX_PATH)
    return shell(cmd, venv=venv)


def doctest(fail_fast=False, venv=None):
    """run `sphinx` doctest"""
    log(INFO, ICONS["doctest"] +
        'run sphinx doctest scripts (only on new or modified files)')
    ff = '' if fail_fast else " --keep-going"
    cmd = "sphinx-build -W %s -b doctest %s %s " % (ff, PATH, BUILD_PATH)
    return shell(cmd, venv=venv)


def show(venv=None):
    """show html documentation"""
    log(INFO, ICONS["show"] +
        'find docs at %s' % join(getcwd(), INDEX_FILE))
    if os_name == 'posix':
        return shell("open %s" % INDEX_FILE, venv=venv)
    if os_name == 'nt':
        return shell("start %s" % INDEX_FILE, venv=venv)
    return 1


def cleanup(venv=None):
    """remove temporary files"""
    log(INFO, ICONS["clean"] + 'clean environment')
    cmd = "sphinx-build -M clean %s %s" % (PATH, BUILD_PATH)
    return shell(cmd, venv=venv)
