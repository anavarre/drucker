# -*- coding: utf-8 -*-
"""Creates mirror image and container"""

from datetime import date
import subprocess as s
import colorful as c
from . import ssh
from . import orchestration as o


def create_base2mirror_container():
    """Create mirror container from base image"""
    print(c.blue("Spinning up %s container with ID:" % (drucker.vars.MIRROR_CONTAINER)))

    create_base2mirror = '''
    docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
    ''' % (drucker.vars.MIRROR_CONTAINER,
           drucker.vars.MIRROR_HOSTNAME,
           drucker.vars.APP,
           drucker.vars.MIRROR_IP,
           drucker.vars.BASE_IMAGE)

    s.run(create_base2mirror, shell=True)

    ssh.configure_ssh_mirror()
    o.run_mirror_orchestration(drucker)


def create_mirror_container():
    """Create mirror container from mirror image"""
    print(c.blue("Spinning up %s container with ID:" % (drucker.vars.MIRROR_CONTAINER)))

    s.run("docker run --privileged=true\
          --name %s -it -h %s --net %s --ip %s\
          -d %s bash" % (drucker.vars.MIRROR_CONTAINER,
                         drucker.vars.MIRROR_HOSTNAME,
                         drucker.vars.APP,
                         drucker.vars.MIRROR_IP,
                         drucker.vars.MIRROR_IMAGE), shell=True)

    ssh.configure_ssh_mirror()
    o.run_mirror_orchestration(drucker)


def create_mirror_image():
    """Create mirror image from mirror container"""
    print(c.blue("Committing %s image from %s container..." % (drucker.vars.MIRROR_IMAGE,
                                                               drucker.vars.MIRROR_CONTAINER)))

    s.run("docker commit -m \"%s on %s\" %s %s" % (drucker.vars.MIRROR_CONTAINER,
                                                   str(date.today()),
                                                   drucker.vars.MIRROR_CONTAINER,
                                                   drucker.vars.MIRROR_IMAGE), shell=True)

    print(c.blue("Deleting initial container..."))
    s.getoutput("docker rm -f %s > /dev/null 2>&1" % (drucker.vars.MIRROR_CONTAINER))
    create_mirror_container()


def start_mirror_container():
    """Start mirror container"""
    s.getoutput("docker start %s > /dev/null 2>&1" % (drucker.vars.MIRROR_CONTAINER))


def provision_mirror_container(drucker):
    """Provision mirror container"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    if s.getoutput("docker ps -a | grep -o %s" % (drucker.vars.MIRROR_CONTAINER)):
        print(c.green("%s container already exists." % (drucker.vars.MIRROR_CONTAINER)))
        if s.getoutput("docker ps | grep -o %s" % (drucker.vars.MIRROR_CONTAINER)):
            o.run_mirror_orchestration(drucker)
        else:
            print(c.blue("Starting %s container..." % (drucker.vars.MIRROR_CONTAINER)))
            start_mirror_container()
            o.run_mirror_orchestration(drucker)
    else:
        if s.getoutput("docker images | awk '{print $1\":\"$2}' | grep %s" % (drucker.vars.MIRROR_IMAGE)):
            print(c.green("%s custom image already exists." % (drucker.vars.MIRROR_IMAGE)))
            create_mirror_container()
        else:
            create_base2mirror_container()
            create_mirror_image()


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_mirror_container(drucker)
