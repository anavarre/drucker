#!/usr/bin/env python3
"""All requirements must be met before running orchestration"""

import sys
import shutil
import subprocess as s
import colorful as c
import variables as v


def check_python_version():
    """A recent version of Python is required"""
    if sys.version_info[0] < 3:
        print(c.red("Python 3 or higher is required to run this application."))
        sys.exit()


def check_required_executables():
    """Both Docker and Ansible need to be installed"""
    for executable in v.EXECUTABLES:
        if not shutil.which(executable):
            print(c.red("%s is required to run this application." % (executable).title()))
            sys.exit()


def check_ansible_version():
    """A recent version of Ansible is required"""
    find_version = "ansible --version | head -n1 | awk '{print $2}' | cut -c -3"
    return_version = s.run(find_version,
                           stdout=s.PIPE,
                           shell=True).stdout.decode('utf-8')

    if return_version < "2.4":
        print(c.red("Ansible 2.4 or later is required to run this application."))
        sys.exit()


def check_hosts_file():
    """The local hosts file must be correctly configured"""

    hosts_file_ips = [v.EDGE_IP,
                      v.SEARCH_IP,
                      v.MIRROR_IP]

    for hosts_file_ip in hosts_file_ips:
        if hosts_file_ip not in open(v.HOSTS).read():
            print("A correctly configured local %s file\
 is required to run this application." % (v.HOSTS))

            hosts_file_suggestion = """
You should add the below entries:

%s    %s
%s   search.local
%s   mirror.local
""" % (v.EDGE_IP, v.DOMAINS, v.SEARCH_IP, v.MIRROR_IP)

            print(hosts_file_suggestion)
            sys.exit()


def check_ssh_config_file():
    """The SSH config file must be correctly configured"""

    ssh_config_ips = [v.BASE_IP,
                      v.EDGE_IP,
                      v.WEB_IP,
                      v.DB_IP,
                      v.SEARCH_IP,
                      v.MIRROR_IP]

    for ssh_config_ip in ssh_config_ips:
        if ssh_config_ip not in open(v.SSH_CONFIG).read():
            print("A correctly configured %s file is required\
 to run this application." % (v.SSH_CONFIG))

            ssh_config_suggestion = """
You should add the below configuration:

Host %s %s %s %s %s %s
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
  LogLevel=error
""" % (v.BASE_IP, v.EDGE_IP, v.WEB_IP, v.DB_IP, v.SEARCH_IP, v.MIRROR_IP)

            print(ssh_config_suggestion)
            sys.exit()


check_python_version()
check_required_executables()
check_ansible_version()
check_hosts_file()
check_ssh_config_file()
