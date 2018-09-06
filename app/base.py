# -*- coding: utf-8 -*-
"""Manages the base image and container"""

import subprocess as s
import colorful as c
from datetime import date
from . import ssh
from . import variables as v
from . import orchestration as o


def create_base_container():
    """Create base container from init image"""
    print(c.blue("Spinning up %s container with ID:" % (v.BASE_CONTAINER)))
    s.run('''
          docker run -d --name %s -it --net %s --ip %s %s bash
          ''' % (v.BASE_CONTAINER,
                 v.APP,
                 v.BASE_IP,
                 v.INIT_IMAGE), shell=True)

    ssh.configure_ssh_base()
    o.run_base_orchestration()


def create_base_image():
    """Create base image from base container"""
    print(c.blue("Committing %s image from %s container..." % (v.BASE_IMAGE, v.BASE_CONTAINER)))
    s.run("docker commit -m \"%s on %s\" %s %s" % (v.BASE_CONTAINER,
                                                   str(date.today()),
                                                   v.BASE_CONTAINER,
                                                   v.BASE_IMAGE), shell=True)


def delete_base_container():
    """Delete base container"""
    print(c.blue("Deleting %s container..." % (v.BASE_CONTAINER)))
    s.getoutput("docker rm -f %s > /dev/null 2>&1" % (v.BASE_CONTAINER))


def delete_init_image():
    """Delete init image"""
    print(c.blue("Deleting %s image..." % (v.INIT_IMAGE)))
    s.getoutput("docker rmi %s > /dev/null 2>&1" % (v.INIT_IMAGE))


def provision_base_container():
    """Set up base container from init image"""
    if s.getoutput(v.CHECK_BASE_IMAGE):
        print(c.green("%s image already exists." % (v.BASE_IMAGE)))

        if s.getoutput(v.CHECK_INIT_IMAGE):
            delete_init_image()
    else:
        if s.getoutput("docker ps -a | grep -o \"%s\"" % (v.BASE_CONTAINER)):
            delete_base_container()
        else:
            create_base_container()
            create_base_image()
            delete_base_container()
            delete_init_image()


def main():
    """Main dispatcher called by the main drucker script."""
    provision_base_container()
