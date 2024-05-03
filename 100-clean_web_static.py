#!/usr/bin/python3
"""
Fabric script for deleting out-of-date archives.
"""

from fabric.api import env, run, local
from datetime import datetime
from os.path import exists

env.hosts = ['54.237.23.243', '3.80.18.18']


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): Number of archives, including the most recent, to keep.

    Returns:
        None
    """
    try:
        number = int(number)
    except ValueError:
        return

    if number < 1:
        number = 1

    versions_dir = "/data/web_static/releases/"
    versions_path = local("ls -t versions", capture=True).split("\n")

    if len(versions_path) <= number:
        return

    # Deleting old archives in the local server
    for old_archive in versions_path[number:]:
        local("rm -f versions/{}".format(old_archive))

    # Deleting old archives on remote servers
    for host in env.hosts:
        with settings(host_string=host):
            run("cd {} && ls -t | tail -n +{} | xargs rm -rf".format(
                versions_dir, number + 1))
