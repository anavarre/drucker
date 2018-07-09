#!/usr/bin/env python3
import colorful as c
import subprocess as s
import variables as v
import ssh
import orchestration as o
from datetime import date

# Get the current path to the ansible.cfg override.
# CONTAINERS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# export ANSIBLE_CONFIG="${CONTAINERS_DIR}/ansible.cfg"

def create_base_container_from_init_image():
    """Create base container from init image"""
    print(c.blue("Spinning up %s container with ID:" % (v.base_container)))
    s.run(v.create_base_container, shell=True)

    ssh.configure_base_container_ssh_access()
    o.run_base_container_orchestration()

def create_base_image_from_base_container():
    """Create base image from base container"""
    today = str(date.today())
    commit_base_image   = "docker commit -m \"%s on %s\" %s %s" % (v.base_container, today, v.base_container, v.base_image)

    print(c.blue("Committing %s image from %s container..." % (v.base_image, v.base_container)))
    s.run(commit_base_image, shell=True)

def delete_base_container():
    """Delete base container"""
    s.getoutput(v.base_container_deletion)

def delete_init_image():
    """Delete init image"""
    s.getoutput(v.init_image_deletion)

def provision_base_container():
    """Set up base container from init image"""
    if s.getoutput(v.check_base_image):
        print(c.green("%s image already exists." % (v.base_image)))

        if s.getoutput(v.check_init_image):
         delete_init_image()
    else:
        if s.getoutput(v.check_base_container):
            delete_base_container()
        else:
            create_base_container_from_init_image()
            create_base_image_from_base_container()
            delete_base_container()
            delete_init_image()

provision_base_container()