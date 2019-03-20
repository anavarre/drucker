#!/usr/bin/env python3
"""Creates edge image and container"""

from datetime import date
import subprocess
import colorful
from . import ssh
from . import orchestration as o


def create_base2edge_container(drucker):
    """Create edge container from base image"""
    print(colorful.white_on_blue("Spinning up %s container with ID:" % (drucker.vars.EDGE_CONTAINER)))

    create_base2edge = '''
                       docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
                       ''' % (drucker.vars.EDGE_CONTAINER,
                              drucker.vars.EDGE_HOSTNAME,
                              drucker.vars.APP,
                              drucker.vars.EDGE_IP,
                              drucker.vars.BASE_IMAGE)

    subprocess.run(create_base2edge, shell=True)

    ssh.configure_ssh_edge(drucker)
    o.run_edge_orchestration(drucker)


def create_edge_container(drucker):
    """Create edge container from edge image"""
    print(colorful.white_on_blue("Spinning up %s container with ID:" % (drucker.vars.EDGE_CONTAINER)))

    subprocess.run("docker run --privileged=true\
                    --name %s -it -h %s --net %s --ip %s\
                    -d %s bash" % (drucker.vars.EDGE_CONTAINER,
                                   drucker.vars.EDGE_HOSTNAME,
                                   drucker.vars.APP,
                                   drucker.vars.EDGE_IP,
                                   drucker.vars.EDGE_IMAGE), shell=True)

    ssh.configure_ssh_edge(drucker)
    o.run_edge_orchestration(drucker)


def create_edge_image(drucker):
    """Create edge image from edge container"""
    print(colorful.white_on_blue("Committing %s image from %s container..."
                                 % (drucker.vars.EDGE_IMAGE,
                                    drucker.vars.EDGE_CONTAINER)))

    subprocess.run("docker commit -m \"%s on %s\" %s %s"
                   % (drucker.vars.EDGE_CONTAINER,
                      str(date.today()),
                      drucker.vars.EDGE_CONTAINER,
                      drucker.vars.EDGE_IMAGE), shell=True)

    print(colorful.white_on_blue("Deleting initial container..."))
    subprocess.getoutput("docker rm -f %s > /dev/null 2>&1" % (drucker.vars.EDGE_CONTAINER))
    create_edge_container(drucker)


def start_edge_container(drucker):
    """Start edge container"""
    subprocess.getoutput("docker start %s > /dev/null 2>&1" % (drucker.vars.EDGE_CONTAINER))


def provision_edge_container(drucker):
    """Provision edge container"""
    if subprocess.getoutput("docker ps -a | grep -o %s" % (drucker.vars.EDGE_CONTAINER)):
        print(colorful.green("%s container already exists." % (drucker.vars.EDGE_CONTAINER)))

        if subprocess.getoutput("docker ps | grep -o %s" % (drucker.vars.EDGE_CONTAINER)):
            o.run_edge_orchestration(drucker)
        else:
            print(colorful.white_on_blue("Starting %s container..." % (drucker.vars.EDGE_CONTAINER)))
            start_edge_container(drucker)
            o.run_edge_orchestration(drucker)
    else:
        if subprocess.getoutput("docker images | awk '{print $1\":\"$2}' | grep %s"
                                % (drucker.vars.EDGE_IMAGE)):
            print(colorful.green("%s custom image already exists." % (drucker.vars.EDGE_IMAGE)))
            create_edge_container(drucker)
        else:
            create_base2edge_container(drucker)
            create_edge_image(drucker)


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_edge_container(drucker)
