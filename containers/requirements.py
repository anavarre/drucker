#!/usr/bin/env python
"""All requirements must be met before running orchestration"""
import sys
import shutil
import subprocess

def check_minimum_python_version():
    """A recent version of Python is required"""
    if sys.version_info[0] < 3:
        print("Python 3 or higher is required to run this application.")
        exit()

def check_required_executables():
    """Both Docker and Ansible need to be installed"""
    executables = ["docker", "ansible"]

    for executable in executables:
        if not shutil.which(executable):
            print("%s is required to run this application." % (executable).title())
            exit()

def check_minimum_ansible_version():
    """A recent version of Ansible is required"""
    find_version = "ansible --version | head -n1 | awk '{print $2}' | cut -c -3"
    return_version = subprocess.run(find_version,
                                    stdout=subprocess.PIPE,
                                    shell=True).stdout.decode('utf-8')

    if return_version < "2.4":
        print("Ansible 2.4 or later is required to run this application.")
        exit()

check_minimum_python_version()
check_required_executables()
check_minimum_ansible_version()
