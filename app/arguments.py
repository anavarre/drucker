#!/usr/bin/env python3
"""Allows to pass arguments to the drucker command"""

import subprocess as s
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


def run_command():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument("app", nargs='?',
                        help="Targets an arbitrary app")

    parser.add_argument('--drupal', dest='drupal', action="store_true",
                        help='Spins up a ready-to-use Drupal install')

    parser.add_argument('--lightning', dest='lightning', action="store_true",
                        help='Spins up a ready-to-use Lightning install')

    parser.add_argument('--blt', dest='blt', action="store_true",
                        help='Spins up a ready-to-use BLT build')

    parser.add_argument('--dev', dest='dev', action="store_true",
                        help='Prepare app for development work with no caching and helper modules enabled.')

    parser.add_argument('--prod', dest='prod', action="store_true",
                        help='Opinionated setup with all known performance best practices enabled.')

    parser.add_argument('--import', dest='import_app', action="store_true",
                        help="Imports an app from the web container's import directory")

    parser.add_argument('--delete', dest='delete', action="store_true",
                        help='Deletes an arbitrary docroot')

    parser.add_argument('--start', dest='start', action="store_true",
                        help='Starts all containers')

    parser.add_argument('--stop', dest='stop', action="store_true",
                        help='Stops all containers')

    parser.add_argument('--restart', dest='restart', action="store_true",
                        help='Restarts all containers')

    parser.add_argument("--health", dest="health", action="store_true",
                        help="Runs a service healthcheck")

    parser.add_argument('--php7.2', dest='php72', action="store_true",
                        help='Sets the PHP version to 7.2')

    parser.add_argument('--php7.1', dest='php71', action="store_true",
                        help='Sets the PHP version to 7.1')

    parser.add_argument('--list', dest='list', action="store_true",
                        help='Lists all deployed apps')

    parser.add_argument('--tests', dest='tests', action="store_true",
                        help='Runs the Ansible test suite')

    parser.add_argument('--version', dest='version', action="store_true",
                        help='Returns the drucker version')

    args = parser.parse_args()

    if args.health:
        containers.health()
    elif args.start:
        containers.start()
    elif args.stop:
        containers.stop()
    elif args.restart:
        containers.restart()
    elif args.php72:
        containers.set_default_php_version()
    elif args.php71:
        containers.set_previous_php_version()
    elif args.list:
        o.app_list()
    elif args.drupal:
        o.app_drupal(args.app)
    elif args.lightning:
        o.app_lightning(args.app)
    elif args.blt:
        o.app_blt(args.app)
    elif args.delete:
        o.app_delete(args.app)
    elif args.dev:
        o.app_dev(args.app)
    elif args.prod:
        o.app_prod(args.app)
    elif args.import_app:
        o.app_import(args.app)
    elif args.tests:
        o.run_tests()
    elif args.version:
        return_version()


run_command()
