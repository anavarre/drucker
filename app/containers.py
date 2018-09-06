#!/usr/bin/env python3
"""Manages containers"""

import subprocess as s
import colorful as c
import variables as v
import services


def status(args):
    """Make sure all containers are started"""
    if s.getoutput("docker ps --format=\"{{.Names}}\"  | grep -c drucker") != "5":
        print(c.red("You cannot run this command when one or more containers are stopped!"))
        start(args)


def health(args):
    """Checks that all required services are up and running"""
    status(args)

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
    return args.exit_ok


def start(args):
    """Starts all containers"""
    for container in v.CONTAINERS:
        if not s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
            print(c.blue("Starting %s container..." % (container)))
            s.getoutput("docker start %s" % (container))
        else:
            print("%s container is already started." % (container))
    health(args)
    return args.exit_ok


def stop(args):
    """Stops all containers"""
    for container in v.CONTAINERS:
        if s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
            print(c.blue("Stopping %s container..." % (container)))
            s.getoutput("docker stop %s" % (container))
        else:
            print("%s container is already stopped." % (container))
    return args.exit_ok


def restart(args):
    """Restarts all containers"""
    for container in v.CONTAINERS:
        if s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
            print(c.blue("Restarting %s container..." % (container)))
            s.getoutput("docker restart %s" % (container))
    health(args)
    return args.exit_ok


def set_previous_php_version(args):
    """Sets the PHP version to the previous version"""
    print(c.blue("Switch to %s..." % (v.PREVIOUS_PHP)))
    s.run('''ansible-playbook -i %s/orchestration/hosts\
             --user=%s %s/orchestration/commands/previous-php.yml\
             --extra-vars "ansible_sudo_pass=%s"
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP), shell=True)
    return args.exit_ok


def set_default_php_version(args):
    """Set the PHP version to the current stable version"""
    # pylint: disable=E1101
    print(c.blue("Switch to %s..." % (v.DEFAULT_PHP)))
    s.run('''ansible-playbook -i %s/orchestration/hosts\
             --user=%s %s/orchestration/commands/default-php.yml\
             --extra-vars "ansible_sudo_pass=%s"
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP), shell=True)
    return args.exit_ok
