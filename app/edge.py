#!/usr/bin/env python3
"""Creates edge image and container"""

from datetime import date
import subprocess as s
import colorful as c
from . import variables as v
from . import ssh
from . import orchestration as o


def create_base2edge_container():
    """Create edge container from base image"""
    print(c.blue("Spinning up %s container with ID:" % (v.EDGE_CONTAINER)))

    create_base2edge = '''
    docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
    ''' % (v.EDGE_CONTAINER,
           v.EDGE_HOSTNAME,
           v.APP,
           v.EDGE_IP,
           v.BASE_IMAGE)

    s.run(create_base2edge, shell=True)

    ssh.configure_ssh_edge()
    o.run_edge_orchestration()


def create_edge_container():
    """Create edge container from edge image"""
    print(c.blue("Spinning up %s container with ID:" % (v.EDGE_CONTAINER)))

    s.run("docker run --privileged=true\
          --name %s -it -h %s --net %s --ip %s\
          -d %s bash" % (v.EDGE_CONTAINER,
                         v.EDGE_HOSTNAME,
                         v.APP,
                         v.EDGE_IP,
                         v.EDGE_IMAGE), shell=True)

    ssh.configure_ssh_edge()
    o.run_edge_orchestration()


def create_edge_image():
    """Create edge image from edge container"""
    print(c.blue("Committing %s image from %s container..." % (v.EDGE_IMAGE,
                                                               v.EDGE_CONTAINER)))

    s.run("docker commit -m \"%s on %s\" %s %s" % (v.EDGE_CONTAINER,
                                                   str(date.today()),
                                                   v.EDGE_CONTAINER,
                                                   v.EDGE_IMAGE), shell=True)

    print(c.blue("Deleting initial container..."))
    s.getoutput("docker rm -f %s > /dev/null 2>&1" % (v.EDGE_CONTAINER))
    create_edge_container()


def start_edge_container():
    """Start edge container"""
    s.getoutput("docker start %s > /dev/null 2>&1" % (v.EDGE_CONTAINER))


def provision_edge_container(drucker):
    """Provision edge container"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    if s.getoutput("docker ps -a | grep -o %s" % (v.EDGE_CONTAINER)):
        print(c.green("%s container already exists." % (v.EDGE_CONTAINER)))

        if s.getoutput("docker ps | grep -o %s" % (v.EDGE_CONTAINER)):
            o.run_edge_orchestration()
        else:
            print(c.blue("Starting %s container..." % (v.EDGE_CONTAINER)))
            start_edge_container()
            o.run_edge_orchestration()
    else:
        if s.getoutput('''
                       docker images | awk '{print $1\":\"$2}' | grep %s
                       ''' % (v.EDGE_IMAGE)):
            print(c.green("%s custom image already exists." % (v.EDGE_IMAGE)))
            create_edge_container()
        else:
            create_base2edge_container()
            create_edge_image()


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_edge_container(drucker)
