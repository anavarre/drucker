#!/usr/bin/env python3
"""Allows to pass arguments to the drucker command"""

import subprocess as s
import sys
import argparse
import colorful as c
import variables as v
import orchestration as o
import containers

def return_version():
    """Returns either the latest commit hash or tagged release"""
    latest_commit = s.getoutput("cd %s && git rev-parse --short HEAD" % (v.APP_ROOT))

    if 'dev' in v.APP_VERSION:
        print("You are running the dev version at commit " + c.orange(latest_commit))
    else:
        print("You are running tagged release " + c.orange(v.APP_VERSION))

def parser():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument("app", nargs='?',
                        help="Targets an arbitrary app")

    parser.add_argument("--health", dest="health", action="store_true",
                        help="Runs a service healthcheck")

    parser.add_argument('--start', dest='start', action="store_true",
                        help='Starts all containers')

    parser.add_argument('--stop', dest='stop', action="store_true",
                        help='Stops all containers')

    parser.add_argument('--restart', dest='restart', action="store_true",
                        help='Restarts all containers')

    parser.add_argument('--delete', dest='delete', action="store_true",
                        help='Deletes an arbitrary docroot')

    parser.add_argument('--version', dest='version', action="store_true",
                        help='Returns the drucker version')

    parser.add_argument('--list', dest='list', action="store_true",
                        help='Lists all deployed apps')

    parser.add_argument('--tests', dest='tests', action="store_true",
                        help='Runs the Ansible test suite')

    args = parser.parse_args()

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
        o.app_delete(args.app)
    elif args.tests:
        o.run_tests()
    elif args.version:
        return_version()

parser()