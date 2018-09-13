# -*- coding: utf-8 -*-
"""Manages containers"""

import subprocess as s
import colorful as c
from . import services


def status(drucker):
    """Make sure all containers are started"""
    if s.getoutput("docker ps --format=\"{{.Names}}\"  | grep -c drucker") != "5":
        print(c.red("You cannot run this command when one or more containers are stopped!"))
        start(drucker)


def health(drucker):
    """Checks that all required services are up and running"""
    status(drucker)

    print(c.blue("Checking services for %s container..." % (drucker.vars.MIRROR_CONTAINER)))
    services.check(drucker.vars.MIRROR_CONTAINER, "apache2", "Apache")
    services.check(drucker.vars.MIRROR_CONTAINER, "apt-cacher-ng", "Apt-Cacher NG")

    print(c.blue("Checking services for %s container..." % (drucker.vars.EDGE_CONTAINER)))
    services.check(drucker.vars.EDGE_CONTAINER, "varnish", "Varnish")
    services.check(drucker.vars.EDGE_CONTAINER, "nginx", "nginx")

    print(c.blue("Checking services for %s container..." % (drucker.vars.DB_CONTAINER)))
    services.check(drucker.vars.DB_CONTAINER, "mysql", "MySQL")
    services.memcached(drucker.vars.DB_CONTAINER)

    print(c.blue("Checking services for %s container..." % (drucker.vars.SEARCH_CONTAINER)))
    services.solr(drucker.vars.SEARCH_CONTAINER)

    print(c.blue("Checking services for %s container..." % (drucker.vars.WEB_CONTAINER)))
    services.check(drucker.vars.WEB_CONTAINER, "apache2", "Apache")
    services.phpfpm(drucker, drucker.vars.DB_CONTAINER)
    return drucker.vars.EXITCODE_OK


def start(drucker):
    """Starts all containers"""
    for container in drucker.vars.CONTAINERS:
        if not s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
            print(c.blue("Starting %s container..." % (container)))
            s.getoutput("docker start %s" % (container))
        else:
            print("%s container is already started." % (container))
    health(drucker)
    return drucker.vars.EXITCODE_OK


def stop(drucker):
    """Stops all containers"""
    for container in drucker.vars.CONTAINERS:
        if s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
            print(c.blue("Stopping %s container..." % (container)))
            s.getoutput("docker stop %s" % (container))
        else:
            print("%s container is already stopped." % (container))
    return drucker.vars.EXITCODE_OK


def restart(drucker):
    """Restarts all containers"""
    for container in drucker.vars.CONTAINERS:
        if s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
            print(c.blue("Restarting %s container..." % (container)))
            s.getoutput("docker restart %s" % (container))
    health(drucker)
    return drucker.vars.EXITCODE_OK


def set_previous_php_version(drucker):
    """Sets the PHP version to the previous version"""
    print(c.blue("Switch to %s..." % (drucker.vars.PREVIOUS_PHP)))
    s.run('''ansible-playbook -i %s/orchestration/hosts\
             --user=%s %s/orchestration/commands/previous-php.yml\
             --extra-vars "ansible_sudo_pass=%s"
          ''' % (drucker.vars.APP_DIR, drucker.vars.APP, drucker.vars.APP_DIR, drucker.vars.APP), shell=True)
    return drucker.vars.EXITCODE_OK


def set_default_php_version(drucker):
    """Set the PHP version to the current stable version"""
    # pylint: disable=E1101
    print(c.blue("Switch to %s..." % (drucker.vars.DEFAULT_PHP)))
    s.run('''ansible-playbook -i %s/orchestration/hosts\
             --user=%s %s/orchestration/commands/default-php.yml\
             --extra-vars "ansible_sudo_pass=%s"
          ''' % (drucker.vars.APP_DIR, drucker.vars.APP, drucker.vars.APP_DIR, drucker.vars.APP), shell=True)
    return drucker.vars.EXITCODE_OK
