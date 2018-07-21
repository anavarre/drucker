#!/usr/bin/env python3
"""Checks if services are correctly running in containers"""

import subprocess as s
import colorful as c
import variables as v

def check(container, service, name):
    """Starts common services if they're down"""
    if not s.getoutput("docker exec -it %s pgrep %s | head -1" % (container, service)):
        print(c.red("!!! %s is down." % (name)) + " Starting...")
        s.getoutput("docker exec -it %s service %s start" % (container, service))
    else:
        print("- %s is up" % (name))


def phpfpm(container):
    """Starts PHP-FPM if it's down"""
    if not s.getoutput('''docker exec -it %s pgrep php-fpm%s | head -1
                       ''' % (v.WEB_CONTAINER,
                              v.DEFAULT_PHP)):
        print(c.red("!!! PHP-FPM is down.") + " Starting...")
        s.getoutput('''docker exec -it %s service php%s-fpm start
                    ''' % (v.WEB_CONTAINER,
                           v.DEFAULT_PHP))
    else:
        print("- PHP-FPM is up")


def memcached(container):
    """Starts memcached if it's down"""
    if not s.getoutput("docker exec -it %s pgrep memcached" % (container)):
        print(c.red("!!! memcached is down.") + " Starting...")
        s.getoutput('''docker exec -it %s memcached -d -u nobody -m 64 -p 11211 127.0.0.1
                    ''' % (container))
    else:
        print("- memcached is up")


def solr(container):
    """Starts Apache Solr if it's down"""
    if not s.getoutput("docker exec -it %s pgrep java" % (container)):
        print(c.red("!!! Apache Solr is down.") + " Starting...")
        s.getoutput('''docker exec -it -u solr %s /opt/solr/bin/solr start
                    ''' % (container))
    else:
        print("- Apache Solr is up")
