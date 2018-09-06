# -*- coding: utf-8 -*-
"""Creates search image and container"""

import subprocess as s
import colorful as c
from datetime import date
from . import ssh
from . import variables as v
from . import orchestration as o


def create_base2search_container():
    """Create search container from base image"""
    print(c.blue("Spinning up %s container with ID:" % (v.SEARCH_CONTAINER)))

    create_base2search = '''
    docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
    ''' % (v.SEARCH_CONTAINER,
           v.SEARCH_HOSTNAME,
           v.APP,
           v.SEARCH_IP,
           v.BASE_IMAGE)

    s.run(create_base2search, shell=True)

    ssh.configure_ssh_search()
    o.run_search_orchestration()


def create_search_container():
    """Create search container from search image"""
    print(c.blue("Spinning up %s container with ID:" % (v.SEARCH_CONTAINER)))

    s.run("docker run --privileged=true\
          --name %s -it -h %s --net %s --ip %s\
          -d %s bash" % (v.SEARCH_CONTAINER,
                         v.SEARCH_HOSTNAME,
                         v.APP,
                         v.SEARCH_IP,
                         v.SEARCH_IMAGE), shell=True)

    ssh.configure_ssh_search()
    o.run_search_orchestration()


def create_search_image():
    """Create search image from search container"""
    print(c.blue("Committing %s image from %s container..." % (v.SEARCH_IMAGE,
                                                               v.SEARCH_CONTAINER)))

    s.run("docker commit -m \"%s on %s\" %s %s" % (v.SEARCH_CONTAINER,
                                                   str(date.today()),
                                                   v.SEARCH_CONTAINER,
                                                   v.SEARCH_IMAGE), shell=True)

    print(c.blue("Deleting initial container..."))
    s.getoutput("docker rm -f %s > /dev/null 2>&1" % (v.SEARCH_CONTAINER))
    create_search_container()


def start_search_container():
    """Start search container"""
    s.getoutput("docker start %s > /dev/null 2>&1" % (v.SEARCH_CONTAINER))


def provision_search_container():
    """Provision search container"""
    if s.getoutput("docker ps -a | grep -o %s" % (v.SEARCH_CONTAINER)):
        print(c.green("%s container already exists." % (v.SEARCH_CONTAINER)))

        if s.getoutput("docker ps | grep -o %s" % (v.SEARCH_CONTAINER)):
            o.run_search_orchestration()
        else:
            print(c.blue("Starting %s container..." % (v.SEARCH_CONTAINER)))
            start_search_container()
            o.run_search_orchestration()
    else:
        if s.getoutput("docker images | awk '{print $1\":\"$2}' | grep %s" % (v.SEARCH_IMAGE)):
            print(c.green("%s custom image already exists." % (v.SEARCH_IMAGE)))
            create_search_container()
        else:
            create_base2search_container()
            create_search_image()


provision_search_container()
