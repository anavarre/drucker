# -*- coding: utf-8 -*-
"""Manages containers"""

import subprocess
import colorful
from . import services


def status(drucker):
    """Make sure all containers are started"""
    if subprocess.getoutput("docker ps --format=\"{{.Names}}\"  | grep -c drucker") != "5":
        print(colorful.red("You cannot run this command when one or more containers are stopped!"))
        start(drucker)


def health(drucker):
    """Checks that all required services are up and running"""
    status(drucker)

    print(colorful.white_on_blue("Checking services for %s container..." % (drucker.vars.MIRROR_CONTAINER)))
    services.check(drucker.vars.MIRROR_CONTAINER, "apache2", "Apache")
    services.check(drucker.vars.MIRROR_CONTAINER, "apt-cacher-ng", "Apt-Cacher NG")

    print(colorful.white_on_blue("Checking services for %s container..." % (drucker.vars.EDGE_CONTAINER)))
    services.check(drucker.vars.EDGE_CONTAINER, "varnish", "Varnish")
    services.check(drucker.vars.EDGE_CONTAINER, "nginx", "nginx")

    print(colorful.white_on_blue("Checking services for %s container..." % (drucker.vars.DB_CONTAINER)))
    services.check(drucker.vars.DB_CONTAINER, "mysql", "MySQL")
    services.memcached(drucker.vars.DB_CONTAINER)

    print(colorful.white_on_blue("Checking services for %s container..." % (drucker.vars.SEARCH_CONTAINER)))
    services.solr(drucker.vars.SEARCH_CONTAINER)

    print(colorful.white_on_blue("Checking services for %s container..." % (drucker.vars.WEB_CONTAINER)))
    services.check(drucker.vars.WEB_CONTAINER, "apache2", "Apache")
    services.phpfpm(drucker)
    return drucker.vars.EXITCODE_OK


def start(drucker):
    """Starts all containers"""
    for container in drucker.vars.CONTAINERS:
        if not subprocess.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                                    ''' % (container)):
            print(colorful.white_on_blue("Starting %s container..." % (container)))
            subprocess.getoutput("docker start %s" % (container))
        else:
            print("%s container is already started." % (container))
    health(drucker)
    return drucker.vars.EXITCODE_OK


def stop(drucker):
    """Stops all containers"""
    for container in drucker.vars.CONTAINERS:
        if subprocess.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                                ''' % (container)):
            print(colorful.white_on_blue("Stopping %s container..." % (container)))
            subprocess.getoutput("docker stop %s" % (container))
        else:
            print("%s container is already stopped." % (container))
    return drucker.vars.EXITCODE_OK


def restart(drucker):
    """Restarts all containers"""
    for container in drucker.vars.CONTAINERS:
        if subprocess.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                                ''' % (container)):
            print(colorful.white_on_blue("Restarting %s container..." % (container)))
            subprocess.getoutput("docker restart %s" % (container))
    health(drucker)
    return drucker.vars.EXITCODE_OK


def set_default_php_version(drucker):
    """Set the PHP version to the current stable version"""
    # pylint: disable=E1101
    print(colorful.white_on_blue("Switch to %s..." % (drucker.vars.DEFAULT_PHP)))
    subprocess.run('''ansible-playbook -i %s/orchestration/hosts\
                      --user=%s %s/orchestration/commands/default-php.yml\
                      --extra-vars "ansible_sudo_pass=%s"
                   ''' % (drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.vars.APP_DIR,
                          drucker.vars.APP), shell=True)
    return drucker.vars.EXITCODE_OK


def set_previous_php_version(drucker):
    """Sets the PHP version to the previous stable version"""
    print(colorful.white_on_blue("Switch to %s..." % (drucker.vars.PREVIOUS_PHP)))
    subprocess.run('''ansible-playbook -i %s/orchestration/hosts\
                      --user=%s %s/orchestration/commands/previous-php.yml\
                      --extra-vars "ansible_sudo_pass=%s"
                   ''' % (drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.vars.APP_DIR,
                          drucker.vars.APP), shell=True)
    return drucker.vars.EXITCODE_OK


def set_legacy_php_version(drucker):
    """Set the PHP version to the legacy stable version"""
    # pylint: disable=E1101
    print(colorful.white_on_blue("Switch to %s..." % (drucker.vars.LEGACY_PHP)))
    subprocess.run('''ansible-playbook -i %s/orchestration/hosts\
                      --user=%s %s/orchestration/commands/legacy-php.yml\
                      --extra-vars "ansible_sudo_pass=%s"
                   ''' % (drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.vars.APP_DIR,
                          drucker.vars.APP), shell=True)
    return drucker.vars.EXITCODE_OK
