# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.9, copyright Saturday, 02 October 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from logging import log, DEBUG, INFO, ERROR
from os import getcwd, chdir
from os.path import exists, join

from dulwich import porcelain
from dulwich.repo import Repo

from .const import ICONS
from .setup_tools import EXT

BRANCH = 'master'


def commit_git(msg='', path=getcwd()):
    """add and commit changes to local `git` repo"""
    cwd = getcwd()
    chdir(path)
    repo = Repo(path) if exists(join(path, '.git')) else Repo.init(path)
    _, files, untracked = porcelain.status(repo)
    repo.stage(files)
    repo.stage(untracked)
    # added, ignored = porcelain.add(repo)
    staged, un_staged, untracked = porcelain.status(repo, False)
    if not any(staged.values()):
        log(INFO, ICONS["missing"] + "not files found - did not commit")
        log(DEBUG, ICONS[""] + "at " + path)
        chdir(cwd)
        return 0

    log(INFO, ICONS["status"] + "file status in `git` repo")
    log(DEBUG, ICONS[""] + "at " + path)

    if staged['add']:
        log(INFO, ICONS[""] + "add:")
        for p in staged['add']:
            log(INFO, ICONS[""] + "  %s" % p.decode())
    if staged['modify']:
        log(INFO, ICONS[""] + "modify:")
        for p in staged['modify']:
            log(INFO, ICONS[""] + "  %s" % p.decode())
    if staged['delete']:
        log(INFO, ICONS[""] + "delete:")
        for p in staged['delete']:
            log(INFO, ICONS[""] + "  %s" % p.decode())
    for p in un_staged:
        log(INFO, ICONS[""] + "unstaged: %s" % p.decode())
    for p in untracked:
        log(INFO, ICONS[""] + "untracked : %s" % p)
    msg = msg if msg else 'Commit'
    msg += EXT
    log(INFO, ICONS["commit"] + "commit changes as `%s`" % msg)
    log(DEBUG, ICONS[""] + "at " + path)
    try:
        res = porcelain.commit(repo, msg)
        log(DEBUG, ICONS[""] + "as %s" % res.decode())
    except Exception as e:
        log(ERROR, ICONS['error'] + str(e))
        chdir(cwd)
        return 1
    chdir(cwd)
    return 0


def tag_git(tag, msg='', path=getcwd()):
    """tag current branch of local `git` repo"""
    log(INFO, ICONS["tag"] + "tag current branch as %s" % tag)
    log(DEBUG, ICONS[""] + "at " + path)
    tag_list = porcelain.tag_list(Repo(path))
    if bytearray(tag.encode()) in tag_list:
        log(ERROR, ICONS["error"] +
            "tag %s exists in current branch of local `git` repo" % tag)
        return 1
    if msg:
        log(DEBUG, ICONS[""] + "msg: `%s`" % msg)
    try:
        porcelain.tag_create(Repo(path), tag, message=msg)
    except Exception as e:
        log(ERROR, ICONS['error'] + str(e))
        return 1
    return 0


def build_url(url, usr='', pwd='None'):   # nosec
    pwd = ':' + str(pwd) if pwd and pwd != 'None' else ''
    usr = str(usr) if usr else 'token-user' if pwd else ''
    remote = \
        'https://' + usr + pwd + '@' + url.replace('https://', '')
    return remote


def clean_url(url):
    http, last = url.split('//', 1)
    usr_pwd, url = last.split('@', 1)
    usr, _ = usr_pwd.split(':', 1) if ':' in usr_pwd else (usr_pwd, '')
    return http + '//' + usr + '@' + url


class Buffer(list):

    def write(self, b):
        self.append(b)


def push_git(remote='None', branch=BRANCH, path=getcwd()):
    """push current branch of local to remote `git` repo"""
    log(INFO, ICONS["push"] + "push current branch to remote `git` repo")
    log(DEBUG, ICONS[""] + "at " + clean_url(remote))

    out = Buffer()

    try:
        porcelain.push(Repo(path), remote, branch, out, out)
    except Exception as e:
        log(ERROR, ICONS['error'] + str(e))
        return 1
    for line in out:
        log(INFO, ICONS[""] + line.decode().strip())
    return 0
