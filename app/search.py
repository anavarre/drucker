# -*- coding: utf-8 -*-
"""Creates search image and container"""

from datetime import date
import subprocess
import colorful
from . import ssh
from . import orchestration as o


def create_base2search_container():
    """Create search container from base image"""
    print(colorful.blue("Spinning up %s container with ID:" % (drucker.vars.SEARCH_CONTAINER)))

    create_base2search = '''
                         docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
                         ''' % (drucker.vars.SEARCH_CONTAINER,
                                drucker.vars.SEARCH_HOSTNAME,
                                drucker.vars.APP,
                                drucker.vars.SEARCH_IP,
                                drucker.vars.BASE_IMAGE)

    subprocess.run(create_base2search, shell=True)

    ssh.configure_ssh_search()
    o.run_search_orchestration(drucker)


def create_search_container():
    """Create search container from search image"""
    print(colorful.blue("Spinning up %s container with ID:" % (drucker.vars.SEARCH_CONTAINER)))

    subprocess.run("docker run --privileged=true\
                    --name %s -it -h %s --net %s --ip %s\
                    -d %s bash" % (drucker.vars.SEARCH_CONTAINER,
                                   drucker.vars.SEARCH_HOSTNAME,
                                   drucker.vars.APP,
                                   drucker.vars.SEARCH_IP,
                                   drucker.vars.SEARCH_IMAGE),
                                   shell=True)

    ssh.configure_ssh_search()
    o.run_search_orchestration(drucker)


def create_search_image():
    """Create search image from search container"""
    print(colorful.blue("Committing %s image from %s container..."
                 % (drucker.vars.SEARCH_IMAGE,
                    drucker.vars.SEARCH_CONTAINER)))

    subprocess.run("docker commit -m \"%s on %s\" %s %s"
                   % (drucker.vars.SEARCH_CONTAINER,
                      str(date.today()),
                      drucker.vars.SEARCH_CONTAINER,
                      drucker.vars.SEARCH_IMAGE), shell=True)

    print(colorful.blue("Deleting initial container..."))
    subprocess.getoutput("docker rm -f %s > /dev/null 2>&1" % (drucker.vars.SEARCH_CONTAINER))
    create_search_container()


def start_search_container():
    """Start search container"""
    subprocess.getoutput("docker start %s > /dev/null 2>&1" % (drucker.vars.SEARCH_CONTAINER))


def provision_search_container(drucker):
    """Provision search container"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    if subprocess.getoutput("docker ps -a | grep -o %s" % (drucker.vars.SEARCH_CONTAINER)):
        print(colorful.green("%s container already exists." % (drucker.vars.SEARCH_CONTAINER)))

        if subprocess.getoutput("docker ps | grep -o %s" % (drucker.vars.SEARCH_CONTAINER)):
            o.run_search_orchestration(drucker)
        else:
            print(colorful.blue("Starting %s container..." % (drucker.vars.SEARCH_CONTAINER)))
            start_search_container()
            o.run_search_orchestration(drucker)
    else:
        if subprocess.getoutput("docker images | awk '{print $1\":\"$2}' | grep %s" % (drucker.vars.SEARCH_IMAGE)):
            print(colorful.green("%s custom image already exists." % (drucker.vars.SEARCH_IMAGE)))
            create_search_container()
        else:
            create_base2search_container()
            create_search_image()


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_search_container(drucker)
