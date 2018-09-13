# -*- coding: utf-8 -*-
"""All requirements must be met before running orchestration"""

import sys
import subprocess
import shutil


def check_python_version():
    """A recent version of Python is required"""
    if sys.version_info[0] < 3:
        raise RuntimeError(
            "Python 3 or higher is required to run this application.")


def check_required_executables(drucker):
    """Both Docker and Ansible need to be installed"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    for executable in drucker.vars.EXECUTABLES:
        if not shutil.which(executable):
            raise RuntimeError(
                "%s is required to run this application."
                % (executable).title())


def check_ansible_version():
    """A recent version of Ansible is required"""
    find_version = "ansible --version | head -n1 | awk '{print $2}' | cut -c -3"
    return_version = subprocess.run(find_version,
                                    stdout=subprocess.PIPE,
                                    shell=True).stdout.decode('utf-8')

    if return_version < "2.4":
        raise RuntimeError(
            "Ansible 2.4 or later is required to run this application.")


def check_hosts_file(drucker):
    """The local hosts file must be correctly configured"""
    hosts_file_ips = [drucker.vars.EDGE_IP,
                      drucker.vars.SEARCH_IP,
                      drucker.vars.MIRROR_IP]
    for hosts_file_ip in hosts_file_ips:
        if hosts_file_ip not in open(drucker.vars.HOSTS).read():
            raise RuntimeError(
                "A correctly configured local {hosts} file"
                " is required to run this application.\n\n"
                "You should add the below entries:\n\n"
                "{edge_ip}    {domains}\n"
                "{search_ip}   search.local\n"
                "{mirror_ip}   mirror.local\n".format(
                    hosts=drucker.vars.HOSTS,
                    edge_ip=drucker.vars.EDGE_IP,
                    domains=drucker.vars.DOMAINS,
                    search_ip=drucker.vars.SEARCH_IP,
                    mirror_ip=drucker.vars.MIRROR_IP))


def check_ssh_config_file(drucker):
    """The SSH config file must be correctly configured"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    ssh_config_ips = [drucker.vars.BASE_IP,
                      drucker.vars.EDGE_IP,
                      drucker.vars.WEB_IP,
                      drucker.vars.DB_IP,
                      drucker.vars.SEARCH_IP,
                      drucker.vars.MIRROR_IP]

    for ssh_config_ip in ssh_config_ips:
        if ssh_config_ip not in open(drucker.vars.SSH_CONFIG).read():
            print("A correctly configured %s file is required\
 to run this application." % (drucker.vars.SSH_CONFIG))

            ssh_config_suggestion = """
You should add the below configuration:

Host %s %s %s %s %s %s
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
  LogLevel=error
""" % (drucker.vars.BASE_IP, drucker.vars.EDGE_IP, drucker.vars.WEB_IP, drucker.vars.DB_IP, drucker.vars.SEARCH_IP, drucker.vars.MIRROR_IP)

            print(ssh_config_suggestion)
            sys.exit()  # TODO: Port to RuntimeError, see check_hosts_file.


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    check_python_version()
    check_required_executables(drucker)
    check_ansible_version()
    check_hosts_file(drucker)
    check_ssh_config_file(drucker)
