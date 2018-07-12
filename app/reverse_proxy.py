#!/usr/bin/env python3
"""Creates reverse proxy image and container"""

import subprocess as s
from datetime import date
import colorful as c
import variables as v
import ssh
import orchestration as o

def create_base2proxy_container():
    """Create reverse proxy container from base image"""
    print(c.blue("Spinning up %s container with ID:" % (v.MIRROR_CONTAINER)))

    create_base2proxy = '''
    docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
    ''' % (v.REVERSE_PROXY_CONTAINER,
           v.REVERSE_PROXY_HOSTNAME,
           v.APP,
           v.REVERSE_PROXY_IP,
           v.BASE_IMAGE)

    s.run(create_base2proxy, shell=True)

    ssh.configure_ssh_reverse_proxy()
    o.run_reverse_proxy_orchestration()

def create_reverse_proxy_container():
    """Create reverse proxy container from reverse proxy image"""
    print(c.blue("Spinning up %s container with ID:" % (v.REVERSE_PROXY_CONTAINER)))

    s.run("docker run --privileged=true\
          --name %s -it -h %s --net %s --ip %s\
          -d %s bash" % (v.REVERSE_PROXY_CONTAINER,
                         v.REVERSE_PROXY_HOSTNAME,
                         v.APP,
                         v.REVERSE_PROXY_IP,
                         v.REVERSE_PROXY_IMAGE), shell=True)

    ssh.configure_ssh_reverse_proxy()
    o.run_reverse_proxy_orchestration()

def create_reverse_proxy_image():
    """Create reverse proxy image from reverse proxy container"""
    print(c.blue("Committing %s image from %s container..." % (v.REVERSE_PROXY_IMAGE,
                                                               v.REVERSE_PROXY_CONTAINER)))

    s.run("docker commit -m \"%s on %s\" %s %s" % (v.REVERSE_PROXY_CONTAINER,
                                                   str(date.today()),
                                                   v.REVERSE_PROXY_CONTAINER,
                                                   v.REVERSE_PROXY_IMAGE), shell=True)

    print(c.blue("Deleting initial container..."))
    s.getoutput("docker rm -f %s > /dev/null 2>&1" % (v.REVERSE_PROXY_CONTAINER))
    create_reverse_proxy_container()

def start_reverse_proxy_container():
    """Start reverse proxy container"""
    s.getoutput("docker start %s > /dev/null 2>&1" % (v.REVERSE_PROXY_CONTAINER))

def provision_reverse_proxy_container():
    """Provision reverse proxy container"""

    """Check if container exists"""
    if s.getoutput("docker ps -a | grep -o %s" % (v.REVERSE_PROXY_CONTAINER)):
        print(c.green("%s container already exists." % (v.REVERSE_PROXY_CONTAINER)))

        """Check if container is started"""
        if s.getoutput("docker ps | grep -o %s" % (v.REVERSE_PROXY_CONTAINER)):
            o.run_reverse_proxy_orchestration()
        else:
            print(c.blue("Starting %s container..." % (v.REVERSE_PROXY_CONTAINER)))
            start_reverse_proxy_container()
            o.run_reverse_proxy_orchestration()
    else:
        if s.getoutput("docker images | awk '{print $1\":\"$2}' | grep %s" % (v.REVERSE_PROXY_IMAGE)):
            print(c.green("%s custom image already exists." % (v.REVERSE_PROXY_IMAGE)))
            create_reverse_proxy_container()
        else:
            create_base2proxy_container()
            create_reverse_proxy_image()

provision_reverse_proxy_container()
