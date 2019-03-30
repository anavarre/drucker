# -*- coding: utf-8 -*-
"""Creates web image and container"""

from datetime import date
import subprocess
import colorful
from . import ssh
from . import orchestration as o


def create_base2web_container(drucker):
    """Create web container from base image"""
    print(
        colorful.white_on_blue(
            "Spinning up %s container with ID:" % (drucker.vars.WEB_CONTAINER)
        )
    )

    create_base2web = """
                      docker run --privileged=true --name %s -it -h %s --net %s --ip %s -d %s bash
                      """ % (
        drucker.vars.WEB_CONTAINER,
        drucker.vars.WEB_HOSTNAME,
        drucker.vars.APP,
        drucker.vars.WEB_IP,
        drucker.vars.BASE_IMAGE,
    )

    subprocess.run(create_base2web, shell=True)

    ssh.configure_ssh_web(drucker)
    o.run_ssh_orchestration(drucker)
    # We need to set up web-to-mirror SSH access to SCP the Drupal Git repo.
    ssh.allow_ssh_access(drucker, drucker.vars.MIRROR_CONTAINER)
    o.run_web_orchestration(drucker)


def create_web_container(drucker):
    """Creates web container from web image"""
    print(
        colorful.white_on_blue(
            "Spinning up %s container with ID:" % (drucker.vars.WEB_CONTAINER)
        )
    )

    subprocess.run(
        "docker run --privileged=true\
                    --name %s -it -h %s --net %s --ip %s\
                    -d -v %s:%s --volumes-from %s %s bash"
        % (
            drucker.vars.WEB_CONTAINER,
            drucker.vars.WEB_HOSTNAME,
            drucker.vars.APP,
            drucker.vars.WEB_IP,
            drucker.vars.HOST_HTML_PATH,
            drucker.vars.CONTAINER_HTML_PATH,
            drucker.vars.DB_CONTAINER,
            drucker.vars.WEB_IMAGE,
        ),
        shell=True,
    )

    ssh.configure_ssh_web(drucker)
    o.run_web_orchestration(drucker)


def create_web_image(drucker):
    """Creates web image from web container"""
    print(
        colorful.white_on_blue(
            "Committing %s image from %s container..."
            % (drucker.vars.WEB_IMAGE, drucker.vars.WEB_CONTAINER)
        )
    )

    subprocess.run(
        'docker commit -m "%s on %s" %s %s'
        % (
            drucker.vars.WEB_CONTAINER,
            str(date.today()),
            drucker.vars.WEB_CONTAINER,
            drucker.vars.WEB_IMAGE,
        ),
        shell=True,
    )

    print(colorful.white_on_blue("Deleting initial container..."))
    subprocess.getoutput(
        "docker rm -f %s > /dev/null 2>&1" % (drucker.vars.WEB_CONTAINER)
    )
    create_web_container(drucker)


def start_web_container(drucker):
    """Starts web container"""
    subprocess.getoutput("docker start %s" % (drucker.vars.WEB_CONTAINER))


def provision_web_container(drucker):
    """Provisions web container"""
    if subprocess.getoutput("docker ps -a | grep -o %s" % (drucker.vars.WEB_CONTAINER)):
        print(
            colorful.green(
                "%s container already exists." % (drucker.vars.WEB_CONTAINER)
            )
        )

        if subprocess.getoutput(
            "docker ps | grep -o %s" % (drucker.vars.WEB_CONTAINER)
        ):
            o.run_web_orchestration(drucker)
        else:
            print(
                colorful.white_on_blue(
                    "Starting %s container..." % (drucker.vars.WEB_CONTAINER)
                )
            )
            start_web_container(drucker)
            o.run_web_orchestration(drucker)
    else:
        if subprocess.getoutput(
            "docker images | awk '{print $1\":\"$2}' | grep %s"
            % (drucker.vars.WEB_IMAGE)
        ):
            print(
                colorful.green(
                    "%s custom image already exists." % (drucker.vars.WEB_IMAGE)
                )
            )
            create_web_container(drucker)
        else:
            create_base2web_container(drucker)
            create_web_image(drucker)


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    provision_web_container(drucker)
    ssh.allow_ssh_access(drucker, drucker.vars.DB_CONTAINER)
