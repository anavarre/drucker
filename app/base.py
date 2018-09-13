# -*- coding: utf-8 -*-
"""Manages the base image and container"""

from datetime import date
import subprocess
import colorful
from . import ssh
from . import orchestration as o


def create_base_container(drucker):
    """Create base container from init image"""
    print(colorful.blue("Spinning up %s container with ID:" % (drucker.vars.BASE_CONTAINER)))
    subprocess.run("docker run -d --name %s -it --net %s --ip %s %s bash"
                   % (drucker.vars.BASE_CONTAINER,
                      drucker.vars.APP,
                      drucker.vars.BASE_IP,
                      drucker.vars.INIT_IMAGE),
                      shell=True)

    ssh.configure_ssh_base(drucker)
    o.run_base_orchestration(drucker)


def create_base_image(drucker):
    """Create base image from base container"""
    print(colorful.blue("Committing %s image from %s container..."
                        % (drucker.vars.BASE_IMAGE,
                           drucker.vars.BASE_CONTAINER)))
    subprocess.run("docker commit -m \"%s on %s\" %s %s"
                   % (drucker.vars.BASE_CONTAINER,
                      str(date.today()),
                      drucker.vars.BASE_CONTAINER,
                      drucker.vars.BASE_IMAGE),
                      shell=True)


def delete_base_container(drucker):
    """Delete base container"""
    print(colorful.blue("Deleting %s container..." % (drucker.vars.BASE_CONTAINER)))
    subprocess.getoutput("docker rm -f %s > /dev/null 2>&1" % (drucker.vars.BASE_CONTAINER))


def delete_init_image(drucker):
    """Delete init image"""
    print(colorful.blue("Deleting %s image..." % (drucker.vars.INIT_IMAGE)))
    subprocess.getoutput("docker rmi %s > /dev/null 2>&1" % (drucker.vars.INIT_IMAGE))


def provision_base_container(drucker):
    """Set up base container from init image"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    if subprocess.getoutput(drucker.vars.CHECK_BASE_IMAGE):
        print(colorful.green("%s image already exists." % (drucker.vars.BASE_IMAGE)))

        if subprocess.getoutput(drucker.vars.CHECK_INIT_IMAGE):
            delete_init_image(drucker)
    else:
        if subprocess.getoutput("docker ps -a | grep -o \"%s\"" % (drucker.vars.BASE_CONTAINER)):
            delete_base_container(drucker)
        else:
            create_base_container(drucker)
            create_base_image(drucker)
            delete_base_container(drucker)
            delete_init_image(drucker)


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_base_container(drucker)
