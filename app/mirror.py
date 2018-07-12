#!/usr/bin/env python3
"""Creates mirror image and container"""

import subprocess as s
from datetime import date
import colorful as c
import variables as v
import ssh
import orchestration as o

def create_base2mirror_container():
    """Create mirror container from base image"""
    print(c.blue("Spinning up %s container with ID:" % (v.MIRROR_CONTAINER)))

    create_base2mirror = '''
    docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
    ''' % (v.MIRROR_CONTAINER,
           v.MIRROR_HOSTNAME,
           v.APP,
           v.MIRROR_IP,
           v.BASE_IMAGE)

    s.run(create_base2mirror, shell=True)

    ssh.configure_ssh_mirror()
    o.run_mirror_orchestration()

def create_mirror_container():
    """Create mirror container from mirror image"""
    print(c.blue("Spinning up ${MIRROR_CONTAINER} container with ID:"))

    s.run("docker run --privileged=true\
          --name %s -it -h %s --net %s --ip %s\
          -d %s bash" % (v.MIRROR_CONTAINER,
                         v.MIRROR_HOSTNAME,
                         v.APP,
                         v.MIRROR_IP,
                         v.BASE_IMAGE), shell=True)

    ssh.configure_ssh_mirror()
    o.run_mirror_orchestration()

def create_mirror_image():
    """Create mirror image from mirror container"""
    print(c.blue("Committing %s image from %s container..." % (v.MIRROR_IMAGE,
                                                                v.MIRROR_CONTAINER)))

    s.run("docker commit -m \"%s on %s\" %s %s" % (v.MIRROR_CONTAINER,
                                                   str(date.today()),
                                                   v.MIRROR_CONTAINER,
                                                   v.MIRROR_IMAGE), shell=True)

    print(c.blue("Deleting initial container..."))
    s.getoutput("docker rm -f %s > /dev/null 2>&1" % (v.MIRROR_CONTAINER))
    create_mirror_container()

def start_mirror_container():
    """Start mirror container"""
    s.getoutput("docker start %s > /dev/null 2>&1" % (v.MIRROR_CONTAINER))

def provision_mirror_container():
    """Provision mirror container"""

    """Check if container exists"""
    if s.getoutput("docker ps -a | grep -o %s" % (v.MIRROR_CONTAINER)):
        print(c.green("%s container already exists." % (v.MIRROR_CONTAINER)))

        """Check if container is started"""
        if s.getoutput("docker ps | grep -o %s" % (v.MIRROR_CONTAINER)):
            o.run_mirror_orchestration()
        else:
            print(c.blue("Starting %s container..." % (v.MIRROR_CONTAINER)))
            start_mirror_container()
            o.run_mirror_orchestration()
    else:
        if s.getoutput("docker images | awk '{print $1\":\"$2}' | grep %s" % (v.MIRROR_IMAGE)):
            print(c.green("%s custom image already exists." % (v.MIRROR_IMAGE)))
            create_mirror_container()
        else:
            create_base2mirror_container()
            create_mirror_image()

provision_mirror_container()
