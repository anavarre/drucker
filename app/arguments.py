#!/usr/bin/env python3
"""Allows to pass arguments to the drucker command"""

import subprocess as s
import colorful as c
import argparse
import variables as v
import sys
import orchestration as o
import containers

p = argparse.ArgumentParser()

p.add_argument('--health',
    dest='health',
    action="store_true",
    help='Runs a service healthcheck')

p.add_argument('--start',
    dest='start',
    action="store_true",
    help='Starts all containers')

p.add_argument('--stop',
    dest='stop',
    action="store_true",
    help='Stops all containers')

p.add_argument('--restart',
    dest='restart',
    action="store_true",
    help='Restarts all containers')

p.add_argument('--list',
    dest='list',
    action="store_true",
    help='Lists all deployed apps')

p.add_argument('--delete',
    dest='delete',
    action="store_true",
    help='Deletes an arbitrary docroot')

p.add_argument('--tests',
    dest='tests',
    action="store_true",
    help='Runs the Ansible test suite')

p.add_argument('--version',
    dest='version',
    action="store_true",
    help='Returns the drucker version')

args = p.parse_args()


def return_version():
    """Returns either the latest commit hash or tagged release"""
    latest_commit= s.getoutput("cd %s && git rev-parse --short HEAD" % (v.APP_ROOT))

    if 'dev' in v.APP_VERSION:
        print("You are running the dev version at commit " + c.orange(latest_commit))
    else:
        print("You are running tagged release " + c.orange(v.APP_VERSION))

if args.health:
    containers.health()
elif args.start:
    containers.start()
elif args.stop:
    containers.stop()
elif args.restart:
    containers.restart()
elif args.list:
    o.app_list()
elif args.delete:
    o.app_delete()
elif args.tests:
    o.run_tests()
elif args.version:
    return_version()
