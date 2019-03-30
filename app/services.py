# -*- coding: utf-8 -*-
"""Checks if services are correctly running in containers"""

import subprocess
import colorful


def check(container, service, name):
    """Starts common services if they're down"""
    if not subprocess.getoutput(
        "docker exec -it %s pgrep %s | head -1" % (container, service)
    ):
        print(colorful.red("!!! %s is down." % (name)) + " Starting...")
        subprocess.getoutput(
            "docker exec -it %s service %s start" % (container, service)
        )
    else:
        print("- %s is up" % (name))


def phpfpm(drucker):
    """Starts PHP-FPM if it's down"""
    if not subprocess.getoutput(
        "docker exec -it %s pgrep php-fpm%s | head -1"
        % (drucker.vars.WEB_CONTAINER, drucker.vars.DEFAULT_PHP)
    ):
        print(colorful.red("!!! PHP-FPM is down.") + " Starting...")
        subprocess.getoutput(
            "docker exec -it %s service php%s-fpm start"
            % (drucker.vars.WEB_CONTAINER, drucker.vars.DEFAULT_PHP)
        )
    else:
        print("- PHP-FPM is up")


def memcached(container):
    """Starts memcached if it's down"""
    if not subprocess.getoutput("docker exec -it %s pgrep memcached" % (container)):
        print(colorful.red("!!! memcached is down.") + " Starting...")
        subprocess.getoutput(
            "docker exec -it %s memcached -d -u nobody -m 64 -p 11211 127.0.0.1"
            % (container)
        )
    else:
        print("- memcached is up")


def solr(container):
    """Starts Apache Solr if it's down"""
    if not subprocess.getoutput("docker exec -it %s pgrep java" % (container)):
        print(colorful.red("!!! Apache Solr is down.") + " Starting...")
        subprocess.getoutput(
            "docker exec -it -u solr %s /opt/solr/bin/solr start" % (container)
        )
    else:
        print("- Apache Solr is up")
