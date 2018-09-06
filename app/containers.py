# -*- coding: utf-8 -*-
"""Manages containers"""

import subprocess as s
import colorful as c
from . import variables as v
from . import services


def status(drucker):
    """Make sure all containers are started"""
    if s.getoutput("docker ps --format=\"{{.Names}}\"  | grep -c drucker") != "5":
        print(c.red("You cannot run this command when one or more containers are stopped!"))
        start(drucker)


def health(drucker):
    """Checks that all required services are up and running"""
    status(drucker)

    print(c.blue("Checking services for %s container..." % (v.MIRROR_CONTAINER)))
    services.check(v.MIRROR_CONTAINER, "apache2", "Apache")
    services.check(v.MIRROR_CONTAINER, "apt-cacher-ng", "Apt-Cacher NG")

    print(c.blue("Checking services for %s container..." % (v.EDGE_CONTAINER)))
    services.check(v.EDGE_CONTAINER, "varnish", "Varnish")
    services.check(v.EDGE_CONTAINER, "nginx", "nginx")

    print(c.blue("Checking services for %s container..." % (v.DB_CONTAINER)))
    services.check(v.DB_CONTAINER, "mysql", "MySQL")
    services.memcached(v.DB_CONTAINER)

    print(c.blue("Checking services for %s container..." % (v.SEARCH_CONTAINER)))
    services.solr(v.SEARCH_CONTAINER)

    print(c.blue("Checking services for %s container..." % (v.WEB_CONTAINER)))
    services.check(v.WEB_CONTAINER, "apache2", "Apache")
    services.phpfpm(v.DB_CONTAINER)
    return drucker.vars.EXITCODE_OK


def start(drucker):
    """Starts all containers"""
    for container in v.CONTAINERS:
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
    for container in v.CONTAINERS:
        if s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
            print(c.blue("Stopping %s container..." % (container)))
            s.getoutput("docker stop %s" % (container))
        else:
            print("%s container is already stopped." % (container))
    return drucker.vars.EXITCODE_OK


def restart(drucker):
    """Restarts all containers"""
    for container in v.CONTAINERS:
        if s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
            print(c.blue("Restarting %s container..." % (container)))
            s.getoutput("docker restart %s" % (container))
    health(drucker)
    return drucker.vars.EXITCODE_OK


def set_previous_php_version(drucker):
    """Sets the PHP version to the previous version"""
    print(c.blue("Switch to %s..." % (v.PREVIOUS_PHP)))
    s.run('''ansible-playbook -i %s/orchestration/hosts\
             --user=%s %s/orchestration/commands/previous-php.yml\
             --extra-vars "ansible_sudo_pass=%s"
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP), shell=True)
    return drucker.vars.EXITCODE_OK


def set_default_php_version(drucker):
    """Set the PHP version to the current stable version"""
    # pylint: disable=E1101
    print(c.blue("Switch to %s..." % (v.DEFAULT_PHP)))
    s.run('''ansible-playbook -i %s/orchestration/hosts\
             --user=%s %s/orchestration/commands/default-php.yml\
             --extra-vars "ansible_sudo_pass=%s"
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP), shell=True)
    return drucker.vars.EXITCODE_OK
