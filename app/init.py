# -*- coding: utf-8 -*-
"""Initialize app with Docker networking and init image"""

import subprocess
import colorful


def create_bridge_network(drucker):
    """Creates a custom bridge network"""
    if subprocess.getoutput(drucker.vars.CHECK_BRIDGE):
        print(
            colorful.green(
                "Custom %s bridge network already exists." % (drucker.vars.APP)
            )
        )
    else:
        print(
            colorful.white_on_blue(
                "Creating custom %s bridge network..." % (drucker.vars.APP)
            )
        )
        subprocess.getoutput(drucker.vars.CREATE_BRIDGE)


def pull_base_image(drucker):
    """Pulls and updates the preferred distribution image from the Docker Hub"""
    distro_image_exists = subprocess.getoutput(drucker.vars.CHECK_DISTRO_IMAGE)
    base_image_exists = subprocess.getoutput(drucker.vars.CHECK_BASE_IMAGE)

    if distro_image_exists and not base_image_exists:
        print(colorful.green("%s image already exists" % (drucker.vars.DISTRO_IMAGE)))
        print(
            colorful.white_on_blue(
                "Check if %s can be updated..." % (drucker.vars.DISTRO_IMAGE)
            )
        )
        subprocess.run(drucker.vars.UPDATE_DISTRO_IMAGE, shell=True)
    elif not distro_image_exists:
        print(
            colorful.white_on_blue(
                "Pulling %s image from Docker Hub..." % (drucker.vars.DISTRO_IMAGE)
            )
        )
        subprocess.run(drucker.vars.PULL_DISTRO_IMAGE, shell=True)


def build_init_image(drucker):
    """Builds the init image from Dockerfile"""
    if subprocess.getoutput(drucker.vars.CHECK_INIT_IMAGE):
        print(colorful.green("%s image already exists." % (drucker.vars.INIT_IMAGE)))
    elif not subprocess.getoutput(drucker.vars.CHECK_BASE_IMAGE):
        print(
            colorful.white_on_blue(
                "Building %s image from Dockerfile..." % (drucker.vars.INIT_IMAGE)
            )
        )
        subprocess.run(
            'docker build -t "%s" %s' % (drucker.vars.INIT_IMAGE, drucker.vars.APP_DIR),
            shell=True,
        )


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    create_bridge_network(drucker)
    pull_base_image(drucker)
    build_init_image(drucker)
