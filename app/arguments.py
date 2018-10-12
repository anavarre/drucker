#!/usr/bin/env python3
"""Parsing of command line arguments passed to the drucker."""

import argparse
import subprocess
import colorful
from . import containers as cont
from . import orchestration as orch


def return_version(drucker):
    """Returns either the latest commit hash or tagged release"""
    latest_commit = subprocess.getoutput("cd %s && git rev-parse --short HEAD"
                                         % (drucker.vars.APP_ROOT))
    if 'dev' in drucker.vars.APP_VERSION:
        commitref = colorful.orange(latest_commit)
        print("You are running the dev version at commit " + commitref)
    else:
        tag = colorful.orange(drucker.vars.APP_VERSION)
        print("You are running tagged release " + tag)
    return drucker.vars.EXITCODE_OK


def get_parser():
    """Returns a ArgumentParser object with command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("app", nargs='?',
                        help="Targets an arbitrary app")
    parser.add_argument('--drupal', dest='dispatched_function', action='store_const',
                        help='Spins up a ready-to-use Drupal install',
                        const=orch.app_drupal)
    parser.add_argument('--lightning', dest='dispatched_function', action='store_const',
                        help='Spins up a ready-to-use Lightning install',
                        const=orch.app_lightning)
    parser.add_argument('--blt', dest='dispatched_function', action='store_const',
                        help='Spins up a ready-to-use BLT build',
                        const=orch.app_blt)
    parser.add_argument('--reinstall', dest='dispatched_function', action='store_const',
                        help='Reinstalls Drupal or the currently installed distribution',
                        const=orch.app_reinstall)
    parser.add_argument('--dev', dest='dispatched_function', action='store_const',
                        help='Configures the app for development use',
                        const=orch.app_dev)
    parser.add_argument('--prod', dest='dispatched_function', action='store_const',
                        help='Configures the app for production use',
                        const=orch.app_prod)
    parser.add_argument('--import', dest='dispatched_function', action='store_const',
                        help="Imports an app from the web container's"
                             " import directory",
                        const=orch.app_import)
    parser.add_argument('--delete', dest='dispatched_function', action='store_const',
                        help='Deletes an arbitrary docroot',
                        const=orch.app_delete)
    parser.add_argument('--start', dest='dispatched_function', action='store_const',
                        help='Starts all containers',
                        const=cont.start)
    parser.add_argument('--stop', dest='dispatched_function', action='store_const',
                        help='Stops all containers',
                        const=cont.stop)
    parser.add_argument('--restart', dest='dispatched_function', action='store_const',
                        help='Restarts all containers',
                        const=cont.restart)
    parser.add_argument("--health", dest='dispatched_function', action='store_const',
                        help="Runs a service healthcheck",
                        const=cont.health)
    parser.add_argument('--php7.2', dest='dispatched_function', action='store_const',
                        help='Sets the PHP version to 7.2',
                        const=cont.set_default_php_version)
    parser.add_argument('--php7.1', dest='dispatched_function', action='store_const',
                        help='Sets the PHP version to 7.1',
                        const=cont.set_previous_php_version)
    parser.add_argument('--list', dest='dispatched_function', action='store_const',
                        help='Lists all deployed apps',
                        const=orch.app_list)
    parser.add_argument('--tests', dest='dispatched_function', action='store_const',
                        help='Runs the Ansible test suite',
                        const=orch.run_tests)
    parser.add_argument('--version', dest='dispatched_function', action='store_const',
                        help='Returns the drucker version',
                        const=return_version)
    return parser
