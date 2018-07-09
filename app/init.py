#!/usr/bin/env python3
import os
import colorful as c
import subprocess as s
import variables as v

base_image_exists = s.getoutput(v.check_base_image)

def create_custom_bridge_network():
    """Creates the drucker bridge network"""
    bridge_exists = s.getoutput(v.check_bridge)

    if bridge_exists:
        print(c.green("Custom %s bridge network already exists." % (v.app)))
    else:
        print(c.blue("Creating custom %s bridge network..." % (v.app)))
        s.getoutput(v.create_bridge)

def pull_base_image_from_docker_hub():
    """Pulls and updates the distro_image"""
    distro_image_exists = s.getoutput(v.check_distro_image)

    if distro_image_exists and not base_image_exists:
        print(c.green("%s image already exists" % (v.distro_image)))
        print(c.blue("Check if %s can be updated..." % (v.distro_image)))
        s.run(v.update_distro_image, shell=True)
    elif not distro_image_exists:
        print(c.blue("Pulling %s image from Docker Hub..." % (v.distro_image)))
        s.run(v.pull_distro_image, shell=True)

def build_init_image():
    """Builds the init image from Dockerfile"""
    init_image_exists = s.getoutput(v.check_init_image)

    build_init_image = "docker build -t \"%s\" %s" % (v.init_image, v.app_dir)

    if init_image_exists:
        print(c.green("%s image already exists." % (v.init_image)))
    elif not base_image_exists:
        print(c.blue("Building %s image from Dockerfile..." % (v.init_image)))
        s.run(build_init_image, shell=True)

create_custom_bridge_network()
pull_base_image_from_docker_hub()
build_init_image()

#CONTAINERS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#export ANSIBLE_CONFIG="${CONTAINERS_DIR}/ansible.cfg"