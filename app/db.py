# -*- coding: utf-8 -*-
"""Creates database image and container"""

import subprocess as s
import colorful as c
from datetime import date
from . import variables as v
from . import ssh
from . import orchestration as o


def create_base2db_container():
    """Create database container from base image"""
    print(c.blue("Spinning up %s container with ID:" % (v.DB_CONTAINER)))

    create_base2db = '''
    docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
    ''' % (v.DB_CONTAINER,
           v.DB_HOSTNAME,
           v.APP,
           v.DB_IP,
           v.BASE_IMAGE)

    s.run(create_base2db, shell=True)

    ssh.configure_ssh_db()
    o.run_db_orchestration()


def create_db_container():
    """Create database container from database image"""
    print(c.blue("Spinning up %s container with ID:" % (v.DB_CONTAINER)))

    s.run("docker run --privileged=true\
          --name %s -it -h %s --net %s --ip %s\
          -d %s bash" % (v.DB_CONTAINER,
                         v.DB_HOSTNAME,
                         v.APP,
                         v.DB_IP,
                         v.DB_IMAGE), shell=True)

    ssh.configure_ssh_db()
    o.run_db_orchestration()


def create_db_image():
    """Create database image from database container"""
    print(c.blue("Committing %s image from %s container..." % (v.DB_IMAGE,
                                                               v.DB_CONTAINER)))

    s.run("docker commit -m \"%s on %s\" %s %s" % (v.DB_CONTAINER,
                                                   str(date.today()),
                                                   v.DB_CONTAINER,
                                                   v.DB_IMAGE), shell=True)

    print(c.blue("Deleting initial container..."))
    s.getoutput("docker rm -f %s > /dev/null 2>&1" % (v.DB_CONTAINER))
    create_db_container()


def start_db_container():
    """Start database container"""
    s.getoutput("docker start %s > /dev/null 2>&1" % (v.DB_CONTAINER))


def provision_db_container(drucker):
    """Provision database container"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    if s.getoutput("docker ps -a | grep -o %s" % (v.DB_CONTAINER)):
        print(c.green("%s container already exists." % (v.DB_CONTAINER)))

        if s.getoutput("docker ps | grep -o %s" % (v.DB_CONTAINER)):
            o.run_db_orchestration()
        else:
            print(c.blue("Starting %s container..." % (v.DB_CONTAINER)))
            start_db_container()
            o.run_db_orchestration()
    else:
        if s.getoutput("docker images | awk '{print $1\":\"$2}' | grep %s" % (v.DB_IMAGE)):
            print(c.green("%s custom image already exists." % (v.DB_IMAGE)))
            create_db_container()
        else:
            create_base2db_container()
            create_db_image()


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_db_container(drucker)
