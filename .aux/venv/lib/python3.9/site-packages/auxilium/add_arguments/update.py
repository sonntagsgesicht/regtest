# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.8, copyright Saturday, 02 October 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from argparse import ArgumentParser
from configparser import ConfigParser


from ..tools.git_tools import commit_git
from ..tools.pip_tools import requirements, install, rollback, upgrade, \
    uninstall
from ..tools.docmaintain_tools import docmaintain


def add_arguments(parser=None, config=ConfigParser()):
    parser = ArgumentParser() if parser is None else parser
    parser.add_argument(
        '--upgrade',
        metavar='PKG',
        nargs='?',
        const=config.getboolean('update', 'upgrade', fallback='pip'),
        help=upgrade.__doc__)
    parser.add_argument(
        '--install',
        action='store_const',
        const=not config.getboolean('update', 'install', fallback=False),
        default=config.getboolean('update', 'install', fallback=False),
        help=install.__doc__)
    parser.add_argument(
        '--requirements',
        action='store_const',
        const=not config.getboolean('update', 'requirements', fallback=False),
        default=config.getboolean('update', 'requirements', fallback=False),
        help=requirements.__doc__)
    parser.add_argument(
        '--header',
        action='store_const',
        const=not config.getboolean('update', 'header', fallback=True),
        default=config.getboolean('update', 'header', fallback=True),
        help=docmaintain.__doc__)
    parser.add_argument(
        '--commit',
        nargs='?',
        metavar='MSG',
        const=None,
        default=config.get('update', 'commit', fallback='Commit'),
        help=commit_git.__doc__)
    ignore = ' (ignores other input)'
    parser.add_argument(
        '--cleanup',
        action='store_const',
        const=not config.getboolean('update', 'cleanup', fallback=False),
        default=config.getboolean('update', 'cleanup', fallback=False),
        help=uninstall.__doc__ + ' and ' + rollback.__doc__ + ignore)
    return parser
