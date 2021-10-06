# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.8, copyright Saturday, 02 October 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from logging import log, basicConfig
from os import getcwd, name as os_name
from os.path import basename
from pathlib import Path
from sys import exit

from argparse import ArgumentParser
from configparser import ConfigParser

from auxilium import add_arguments
from auxilium.add_arguments import ArgumentDefaultsAndConstsHelpFormatter
from auxilium.methods.root import do
from auxilium.tools.const import CONFIG_PATH, VERBOSITY_LEVELS, ICONS


def main():

    # ==========================
    # === init config parser ===
    # ==========================

    config = ConfigParser(allow_no_value=True)
    config.read(Path.home().joinpath(CONFIG_PATH))
    config.read(CONFIG_PATH)

    if not config.getboolean('DEFAULT', 'icons', fallback=os_name == 'posix'):
        ICONS.clear()
        ICONS.update({'error': '!!', 'warn': '!'})

    # ===========================
    # === add argument parser ===
    # ===========================

    epilog = """
if (default: True) a given flag turns its value to False. \
default behavior may depend on current path and project.
set default behavior in `~/%s` and `./%s`."
""" % (CONFIG_PATH, CONFIG_PATH)

    description = """
creates and manages boilerplate python development workflow.
 [ create > exit_status > test > build > deploy ]
"""

    parser = ArgumentParser(
        epilog=epilog,
        description=description,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter)

    sub_parser = parser.add_subparsers(dest='command')

    # === create ===
    help = "creates a new project, repo and virtual environment"
    description = help + """ \
with project file structure from templates which has already set-up
 `venv` virtual python environment to run and test projects isolated
 `git` source exit_status repository for tracking source exit_status changes
 `unittest` suite of tests to ensure the project works as intended
  already-to-use documentation structure build for `sphinx`
"""

    sub_parser.add_parser(
        'create',
        epilog=epilog,
        description=description,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help=description)

    # === update ===
    description = "keeps project, repo and dependencies up-to-date"
    sub_parser.add_parser(
        'update',
        epilog=epilog,
        description=description,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help=description)

    # === test ==
    description = "checks project integrity " \
                  "by testing using `unittest` framework"
    sub_parser.add_parser(
        'test',
        epilog=epilog,
        description=description,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help=description)

    # === documentation ==
    description = "builds project documentation using `sphinx`"
    sub_parser.add_parser(
        'doc',
        epilog=epilog,
        description=description,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help=description)

    # === deploy ==
    description = "builds project distribution " \
                  "and deploy releases to `pypi.org`"
    sub_parser.add_parser(
        'build',
        epilog=epilog,
        description=description,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help=description)

    # === invoke python ==
    description = "invokes python in virtual environment"
    sub_parser.add_parser(
        'python',
        epilog='Call python interpreter of virtual environment '
               '(Note: only some standard optional arguments are implemented)',
        description=description,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help=description)

    # ===============================
    # === add arguments to parser ===
    # ===============================

    method = getattr(add_arguments, 'root', None)
    method(parser, config) if method else None

    for k, v in sub_parser.choices.items():
        method = getattr(add_arguments, k, None)
        method(v, config) if method else None

    # ===============================
    # === invoke parsed arguments ===
    # ===============================

    # pars arguments
    args = parser.parse_args()
    kwargs = vars(args)

    # add pkg and path to kwargs
    kwargs['cwd'] = kwargs.get('cwd', getcwd())
    kwargs['path'] = kwargs.get('path', getcwd())
    kwargs['pkg'] = kwargs.get('name', basename(getcwd()))

    # init logging
    item = min(args.verbosity, len(VERBOSITY_LEVELS) - 1)
    verbosity, formatter = VERBOSITY_LEVELS[item]
    basicConfig(level=verbosity, format=formatter)
    log(1, ICONS['inspect'] + '(parsed) arguments:')
    for item in kwargs.items():
        log(1, ICONS[''] + "  %-12s : %r" % item)

    # print help in case of no command
    if args.command is None and not args.demo:
        parser.print_help()
        for p in sub_parser.choices.values():
            p.print_help()
        exit()

    # call command/method
    do(**kwargs)


if __name__ == '__main__':
    main()
