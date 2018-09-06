#!/usr/bin/env python3
"""Parsing of command line arguments passed to the drucker."""

import sys
import argparse
import subprocess
import colorful
import variables
import containers
import orchestration


def return_version(args):
    """Returns either the latest commit hash or tagged release"""
    latest_commit = subprocess.getoutput("cd %s && git rev-parse --short HEAD"
                                         % (variables.APP_ROOT))
    if 'dev' in variables.APP_VERSION:
        ver = colorful.orange(latest_commit)
        print("You are running the dev version at commit " + ver)
    else:
        ver = colorful.orange(variables.APP_VERSION)
        print("You are running tagged release " + ver)
    return args.exit_ok


def get_parser():
    """Returns a ArgumentParser object with command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("app", nargs='?',
                        help="Targets an arbitrary app")
    parser.add_argument('--drupal', dest='mainfunc', action='store_const',
                        help='Spins up a ready-to-use Drupal install',
                        const=orchestration.app_drupal)
    parser.add_argument('--lightning', dest='mainfunc', action='store_const',
                        help='Spins up a ready-to-use Lightning install',
                        const=orchestration.app_lightning)
    parser.add_argument('--blt', dest='mainfunc', action='store_const',
                        help='Spins up a ready-to-use BLT build',
                        const=orchestration.app_blt)
    parser.add_argument('--dev', dest='mainfunc', action='store_const',
                        help='Prepare app for development work with no'
                             ' caching and helper modules enabled.',
                        const=orchestration.app_dev)
    parser.add_argument('--prod', dest='mainfunc', action='store_const',
                        help='Opinionated setup with all known performance'
                             ' best practices enabled.',
                        const=orchestration.app_prod)
    parser.add_argument('--import', dest='mainfunc', action='store_const',
                        help="Imports an app from the web container's"
                             " import directory",
                        const=orchestration.app_import)
    parser.add_argument('--delete', dest='mainfunc', action='store_const',
                        help='Deletes an arbitrary docroot',
                        const=orchestration.app_delete)
    parser.add_argument('--start', dest='mainfunc', action='store_const',
                        help='Starts all containers',
                        const=containers.start)
    parser.add_argument('--stop', dest='mainfunc', action='store_const',
                        help='Stops all containers',
                        const=containers.stop)
    parser.add_argument('--restart', dest='mainfunc', action='store_const',
                        help='Restarts all containers',
                        const=containers.restart)
    parser.add_argument("--health", dest='mainfunc', action='store_const',
                        help="Runs a service healthcheck",
                        const=containers.health)
    parser.add_argument('--php7.2', dest='mainfunc', action='store_const',
                        help='Sets the PHP version to 7.2',
                        const=containers.set_default_php_version)
    parser.add_argument('--php7.1', dest='mainfunc', action='store_const',
                        help='Sets the PHP version to 7.1',
                        const=containers.set_previous_php_version)
    parser.add_argument('--list', dest='mainfunc', action='store_const',
                        help='Lists all deployed apps',
                        const=orchestration.app_list)
    parser.add_argument('--tests', dest='mainfunc', action='store_const',
                        help='Runs the Ansible test suite',
                        const=orchestration.run_tests)
    parser.add_argument('--version', dest='mainfunc', action='store_const',
                        help='Returns the drucker version',
                        const=return_version)
    return parser


if __name__ == '__main__':
    PARSER = get_parser()
    ARGS = PARSER.parse_args()
    # Define convenience constants for UNIX exit codes so that third-party
    # developers can use Drucker in scripts:
    # http://tldp.org/LDP/abs/html/exitcodes.html
    ARGS.exit_ok = 0
    ARGS.exit_fail = 1
    # Dispatch program execution to the chosen option and send args to it.
    EXITCODE = ARGS.mainfunc(ARGS)
    sys.exit(EXITCODE)
