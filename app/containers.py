#!/usr/bin/env python3
"""Manages containers"""

import sys
import subprocess as s
import variables as v
import colorful as c
import services

def status():
    """Make sure all containers are started"""
    if s.getoutput("docker ps --format=\"{{.Names}}\"  | grep -c drucker") != "5":
        print(c.red("You cannot run this command when one or more containers are stopped!"))
        start()

def health():
    """Checks that all required services are up and running"""
    status()

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


def start():
    """Starts all containers"""
    for container in v.CONTAINERS:
        if not s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
           print(c.blue("Starting %s container..." % (container)))
           s.getoutput("docker start %s" % (container))
        else:
            print("%s container is already started." % (container))
    health()


def stop():
    """Stops all containers"""
    for container in v.CONTAINERS:
        if s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
           print(c.blue("Stopping %s container..." % (container)))
           s.getoutput("docker stop %s" % (container))
        else:
            print("%s container is already stopped." % (container))


def restart():
    """Restarts all containers"""
    for container in v.CONTAINERS:
        if s.getoutput('''docker ps --format=\"{{.Names}}\"  | grep %s
                           ''' % (container)):
           print(c.blue("Restarting %s container..." % (container)))
           s.getoutput("docker restart %s" % (container))
    health()
