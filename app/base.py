# -*- coding: utf-8 -*-
"""Manages the base image and container"""

from datetime import date
import subprocess
import colorful
from . import ssh
from . import orchestration as o


def create_base_container():
    """Create base container from init image"""
    print(colorful.blue("Spinning up %s container with ID:" % (drucker.vars.BASE_CONTAINER)))
    subprocess.run("docker run -d --name %s -it --net %s --ip %s %s bash"
                   % (drucker.vars.BASE_CONTAINER,
                      drucker.vars.APP,
                      drucker.vars.BASE_IP,
                      drucker.vars.INIT_IMAGE),
                      shell=True)

    ssh.configure_ssh_base()
    o.run_base_orchestration()


def create_base_image():
    """Create base image from base container"""
    print(colorful.blue("Committing %s image from %s container..." % (drucker.vars.BASE_IMAGE, drucker.vars.BASE_CONTAINER)))
    subprocess.run("docker commit -m \"%s on %s\" %s %s"
                   % (drucker.vars.BASE_CONTAINER,
                      str(date.today()),
                      drucker.vars.BASE_CONTAINER,
                      drucker.vars.BASE_IMAGE),
                      shell=True)


def delete_base_container():
    """Delete base container"""
    print(colorful.blue("Deleting %s container..." % (drucker.vars.BASE_CONTAINER)))
    subprocess.getoutput("docker rm -f %s > /dev/null 2>&1" % (drucker.vars.BASE_CONTAINER))


def delete_init_image():
    """Delete init image"""
    print(colorful.blue("Deleting %s image..." % (drucker.vars.INIT_IMAGE)))
    subprocess.getoutput("docker rmi %s > /dev/null 2>&1" % (drucker.vars.INIT_IMAGE))


def provision_base_container(drucker):
    """Set up base container from init image"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    if subprocess.getoutput(drucker.vars.CHECK_BASE_IMAGE):
        print(colorful.green("%s image already exists." % (drucker.vars.BASE_IMAGE)))

        if subprocess.getoutput(drucker.vars.CHECK_INIT_IMAGE):
            delete_init_image()
    else:
        if subprocess.getoutput("docker ps -a | grep -o \"%s\"" % (drucker.vars.BASE_CONTAINER)):
            delete_base_container()
        else:
            create_base_container()
            create_base_image()
            delete_base_container()
            delete_init_image()


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_base_container(drucker)
