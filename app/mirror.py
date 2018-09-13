# -*- coding: utf-8 -*-
"""Creates mirror image and container"""

from datetime import date
import subprocess
import colorful
from . import ssh
from . import orchestration as o


def create_base2mirror_container(drucker):
    """Create mirror container from base image"""
    print(colorful.blue("Spinning up %s container with ID:" % (drucker.vars.MIRROR_CONTAINER)))

    create_base2mirror = '''
                         docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
                         ''' % (drucker.vars.MIRROR_CONTAINER,
                                drucker.vars.MIRROR_HOSTNAME,
                                drucker.vars.APP,
                                drucker.vars.MIRROR_IP,
                                drucker.vars.BASE_IMAGE)

    subprocess.run(create_base2mirror, shell=True)

    ssh.configure_ssh_mirror(drucker)
    o.run_mirror_orchestration(drucker)


def create_mirror_container(drucker):
    """Create mirror container from mirror image"""
    print(colorful.blue("Spinning up %s container with ID:" % (drucker.vars.MIRROR_CONTAINER)))

    subprocess.run("docker run --privileged=true\
                    --name %s -it -h %s --net %s --ip %s\
                    -d %s bash" % (drucker.vars.MIRROR_CONTAINER,
                                   drucker.vars.MIRROR_HOSTNAME,
                                   drucker.vars.APP,
                                   drucker.vars.MIRROR_IP,
                                   drucker.vars.MIRROR_IMAGE), shell=True)

    ssh.configure_ssh_mirror(drucker)
    o.run_mirror_orchestration(drucker)


def create_mirror_image(drucker):
    """Create mirror image from mirror container"""
    print(colorful.blue("Committing %s image from %s container..."
                        % (drucker.vars.MIRROR_IMAGE,
                           drucker.vars.MIRROR_CONTAINER)))

    subprocess.run("docker commit -m \"%s on %s\" %s %s"
                   % (drucker.vars.MIRROR_CONTAINER,
                      str(date.today()),
                      drucker.vars.MIRROR_CONTAINER,
                      drucker.vars.MIRROR_IMAGE), shell=True)

    print(colorful.blue("Deleting initial container..."))
    subprocess.getoutput("docker rm -f %s > /dev/null 2>&1" % (drucker.vars.MIRROR_CONTAINER))
    create_mirror_container(drucker)


def start_mirror_container(drucker):
    """Start mirror container"""
    subprocess.getoutput("docker start %s > /dev/null 2>&1" % (drucker.vars.MIRROR_CONTAINER))


def provision_mirror_container(drucker):
    """Provision mirror container"""
    if subprocess.getoutput("docker ps -a | grep -o %s" % (drucker.vars.MIRROR_CONTAINER)):
        print(colorful.green("%s container already exists." % (drucker.vars.MIRROR_CONTAINER)))
        if subprocess.getoutput("docker ps | grep -o %s" % (drucker.vars.MIRROR_CONTAINER)):
            o.run_mirror_orchestration(drucker)
        else:
            print(colorful.blue("Starting %s container..." % (drucker.vars.MIRROR_CONTAINER)))
            start_mirror_container(drucker)
            o.run_mirror_orchestration(drucker)
    else:
        if subprocess.getoutput("docker images | awk '{print $1\":\"$2}' | grep %s" % (drucker.vars.MIRROR_IMAGE)):
            print(colorful.green("%s custom image already exists." % (drucker.vars.MIRROR_IMAGE)))
            create_mirror_container(drucker)
        else:
            create_base2mirror_container(drucker)
            create_mirror_image(drucker)


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_mirror_container(drucker)
