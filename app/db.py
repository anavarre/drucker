# -*- coding: utf-8 -*-
"""Creates database image and container"""

from datetime import date
import subprocess
import colorful
from . import ssh
from . import orchestration as o


def create_base2db_container(drucker):
    """Create database container from base image"""
    print(colorful.white_on_blue("Spinning up %s container with ID:" % (drucker.vars.DB_CONTAINER)))

    create_base2db = '''
                     docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
                     ''' % (drucker.vars.DB_CONTAINER,
                            drucker.vars.DB_HOSTNAME,
                            drucker.vars.APP,
                            drucker.vars.DB_IP,
                            drucker.vars.BASE_IMAGE)

    subprocess.run(create_base2db, shell=True)

    ssh.configure_ssh_db(drucker)
    o.run_db_orchestration(drucker)


def create_db_container(drucker):
    """Create database container from database image"""
    print(colorful.white_on_blue("Spinning up %s container with ID:" % (drucker.vars.DB_CONTAINER)))

    subprocess.run("docker run --privileged=true\
                    --name %s -it -h %s --net %s --ip %s\
                    -d %s bash" % (drucker.vars.DB_CONTAINER,
                                   drucker.vars.DB_HOSTNAME,
                                   drucker.vars.APP,
                                   drucker.vars.DB_IP,
                                   drucker.vars.DB_IMAGE), shell=True)

    ssh.configure_ssh_db(drucker)
    o.run_db_orchestration(drucker)


def create_db_image(drucker):
    """Create database image from database container"""
    print(colorful.white_on_blue("Committing %s image from %s container..."
                                 % (drucker.vars.DB_IMAGE,
                                    drucker.vars.DB_CONTAINER)))

    subprocess.run("docker commit -m \"%s on %s\" %s %s"
                   % (drucker.vars.DB_CONTAINER,
                      str(date.today()),
                      drucker.vars.DB_CONTAINER,
                      drucker.vars.DB_IMAGE), shell=True)

    print(colorful.white_on_blue("Deleting initial container..."))
    subprocess.getoutput("docker rm -f %s > /dev/null 2>&1" % (drucker.vars.DB_CONTAINER))
    create_db_container(drucker)


def start_db_container(drucker):
    """Start database container"""
    subprocess.getoutput("docker start %s > /dev/null 2>&1" % (drucker.vars.DB_CONTAINER))


def provision_db_container(drucker):
    """Provision database container"""
    if subprocess.getoutput("docker ps -a | grep -o %s" % (drucker.vars.DB_CONTAINER)):
        print(colorful.green("%s container already exists." % (drucker.vars.DB_CONTAINER)))

        if subprocess.getoutput("docker ps | grep -o %s" % (drucker.vars.DB_CONTAINER)):
            o.run_db_orchestration(drucker)
        else:
            print(colorful.white_on_blue("Starting %s container..." % (drucker.vars.DB_CONTAINER)))
            start_db_container(drucker)
            o.run_db_orchestration(drucker)
    else:
        if subprocess.getoutput("docker images | awk '{print $1\":\"$2}' | grep %s" % (drucker.vars.DB_IMAGE)):
            print(colorful.green("%s custom image already exists." % (drucker.vars.DB_IMAGE)))
            create_db_container(drucker)
        else:
            create_base2db_container(drucker)
            create_db_image(drucker)


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_db_container(drucker)
