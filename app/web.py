# -*- coding: utf-8 -*-
"""Creates web image and container"""

import subprocess as s
import colorful as c
from datetime import date
from . import variables as v
from . import ssh
from . import orchestration as o


def create_base2web_container(drucker):
    """Create web container from base image"""
    print(c.blue("Spinning up %s container with ID:" % (v.WEB_CONTAINER)))

    create_base2web = '''
    docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
    ''' % (v.WEB_CONTAINER,
           v.WEB_HOSTNAME,
           v.APP,
           v.WEB_IP,
           v.BASE_IMAGE)

    s.run(create_base2web, shell=True)

    ssh.configure_ssh_web()
    o.run_ssh_orchestration()
    # We need to set up web-to-mirror SSH access to SCP the Drupal Git repo.
    ssh.allow_ssh_access(drucker, v.MIRROR_CONTAINER)
    o.run_web_orchestration()


def create_web_container():
    """Creates web container from web image"""
    print(c.blue("Spinning up %s container with ID:" % (v.WEB_CONTAINER)))

    s.run("docker run --privileged=true\
          --name %s -it -h %s --net %s --ip %s\
          -d -v %s:%s --volumes-from %s %s bash" % (v.WEB_CONTAINER,
                                                    v.WEB_HOSTNAME,
                                                    v.APP,
                                                    v.WEB_IP,
                                                    v.HOST_HTML_PATH,
                                                    v.CONTAINER_HTML_PATH,
                                                    v.DB_CONTAINER,
                                                    v.WEB_IMAGE), shell=True)

    ssh.configure_ssh_web()
    o.run_web_orchestration()


def create_web_image():
    """Creates web image from web container"""
    print(c.blue("Committing %s image from %s container..." % (v.WEB_IMAGE,
                                                               v.WEB_CONTAINER)))

    s.run("docker commit -m \"%s on %s\" %s %s" % (v.WEB_CONTAINER,
                                                   str(date.today()),
                                                   v.WEB_CONTAINER,
                                                   v.WEB_IMAGE), shell=True)

    print(c.blue("Deleting initial container..."))
    s.getoutput("docker rm -f %s > /dev/null 2>&1" % (v.WEB_CONTAINER))
    create_web_container()


def start_web_container():
    """Starts web container"""
    s.getoutput("docker start %s" % (v.WEB_CONTAINER))


def provision_web_container(drucker):
    """Provisions web container"""
    if s.getoutput("docker ps -a | grep -o %s" % (v.WEB_CONTAINER)):
        print(c.green("%s container already exists." % (v.WEB_CONTAINER)))

        if s.getoutput("docker ps | grep -o %s" % (v.WEB_CONTAINER)):
            o.run_web_orchestration()
        else:
            print(c.blue("Starting %s container..." % (v.WEB_CONTAINER)))
            start_web_container()
            o.run_web_orchestration()
    else:
        if s.getoutput("docker images | awk '{print $1\":\"$2}' | grep %s" % (v.WEB_IMAGE)):
            print(c.green("%s custom image already exists." % (v.WEB_IMAGE)))
            create_web_container()
        else:
            create_base2web_container(drucker)
            create_web_image()


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_web_container(drucker)
    ssh.allow_ssh_access(drucker, v.DB_CONTAINER)
