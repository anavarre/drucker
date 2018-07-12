#!/usr/bin/env python3
"""Manages orchestration for all containers"""

import subprocess as s
import colorful as c
import variables as v

def run_orchestration(container, shortname):
    """Parent function to manage container orchestration"""
    print(c.blue("Running %s orchestration on the container..." % (container)))
    s.getoutput("export ANSIBLE_HOST_KEY_CHECKING=False")
    s.run('''
    ansible-playbook -i %s/orchestration/hosts --user=%s %s/orchestration/provisioning/%s.yml --extra-vars ansible_sudo_pass=%s
    ''' % (v.APP_DIR, v.APP, v.APP_DIR, shortname, v.APP), shell=True)

def run_base_orchestration():
    """Run orchestration on base container"""
    run_orchestration(v.BASE_CONTAINER, "base")

def run_mirror_orchestration():
    """Run orchestration on mirror container"""
    run_orchestration(v.MIRROR_CONTAINER, "mirror")

def run_edge_orchestration():
    """Run orchestration on edge container"""
    run_orchestration(v.EDGE_CONTAINER, "edge")

def run_db_orchestration():
    """Run orchestration on database container"""
    run_orchestration(v.DB_CONTAINER, "db")

def run_web_orchestration():
    """Run orchestration on web container"""
    run_orchestration(v.WEB_CONTAINER, "web")

def run_search_orchestration():
    """Run orchestration on search container"""
    run_orchestration(v.SEARCH_CONTAINER, "search")

def run_ssh_orchestration():
    """Run SSH orchestration"""
    run_orchestration("SSH", "ssh")
