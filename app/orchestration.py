#!/usr/bin/env python3
import variables as v
import colorful as c
import subprocess as s

playbooks         = "ansible-playbook -i %s/orchestration/hosts --user=%s %s/orchestration" % (v.app_dir, v.app, v.app_dir)
host_key_checking = "export ANSIBLE_HOST_KEY_CHECKING=False"
provisioning      = "%s/provisioning" % (playbooks)

def run_base_container_orchestration():
    """Run orchestration on base container"""
    base_container_orchestration = "%s/base.yml --extra-vars ansible_sudo_pass=%s" % (provisioning, v.app)

    print(c.blue("Running %s orchestration on the container..." % (v.base_container)))

    s.getoutput(host_key_checking)
    s.run(base_container_orchestration, shell=True)