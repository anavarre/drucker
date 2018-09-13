# -*- coding: utf-8 -*-
"""Initialize app with Docker networking and init image"""

import subprocess as s
import colorful as c


def create_bridge_network(drucker):
    """Creates a custom bridge network"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    if s.getoutput(drucker.vars.CHECK_BRIDGE):
        print(c.green("Custom %s bridge network already exists." % (drucker.vars.APP)))
    else:
        print(c.blue("Creating custom %s bridge network..." % (drucker.vars.APP)))
        s.getoutput(drucker.vars.CREATE_BRIDGE)


def pull_base_image(drucker):
    """Pulls and updates the preferred distribution image from the Docker Hub"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    distro_image_exists = s.getoutput(drucker.vars.CHECK_DISTRO_IMAGE)
    base_image_exists = s.getoutput(drucker.vars.CHECK_BASE_IMAGE)

    if distro_image_exists and not base_image_exists:
        print(c.green("%s image already exists" % (drucker.vars.DISTRO_IMAGE)))
        print(c.blue("Check if %s can be updated..." % (drucker.vars.DISTRO_IMAGE)))
        s.run(drucker.vars.UPDATE_DISTRO_IMAGE, shell=True)
    elif not distro_image_exists:
        print(c.blue("Pulling %s image from Docker Hub..." % (drucker.vars.DISTRO_IMAGE)))
        s.run(drucker.vars.PULL_DISTRO_IMAGE, shell=True)


def build_init_image(drucker):
    """Builds the init image from Dockerfile"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    if s.getoutput(drucker.vars.CHECK_INIT_IMAGE):
        print(c.green("%s image already exists." % (drucker.vars.INIT_IMAGE)))
    elif not s.getoutput(drucker.vars.CHECK_BASE_IMAGE):
        print(c.blue("Building %s image from Dockerfile..." % (drucker.vars.INIT_IMAGE)))
        s.run("docker build -t \"%s\" %s" % (drucker.vars.INIT_IMAGE, drucker.vars.APP_DIR), shell=True)


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    create_bridge_network(drucker)
    pull_base_image(drucker)
    build_init_image(drucker)
