#!/usr/bin/env python3
"""All requirements must be met before running orchestration"""
import sys
import shutil
import subprocess as s
import colorful as c
import variables as v

def check_minimum_python_version():
    """A recent version of Python is required"""
    if sys.version_info[0] < 3:
        print(c.red("Python 3 or higher is required to run this application."))
        sys.exit()

def check_required_executables():
    """Both Docker and Ansible need to be installed"""
    for executable in v.executables:
        if not shutil.which(executable):
            print(c.red("%s is required to run this application." % (executable).title()))
            sys.exit()

def check_minimum_ansible_version():
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

    hosts_file_ip_addresses = [v.reverse_proxy_ip,
                               v.search_ip,
                               v.mirror_ip]

    for hosts_file_ip_address in hosts_file_ip_addresses:
        if hosts_file_ip_address not in open(v.hosts).read():
            print("A correctly configured local %s file\
 is required to run this application." % (v.hosts))

            hosts_file_suggestion = """
You should add the below entries:

%s    %s
%s   search.local
%s   mirror.local
""" % (v.reverse_proxy_ip,
       v.domains,
       v.search_ip,
       v.mirror_ip)

            print(hosts_file_suggestion)
            sys.exit()

def check_ssh_config_file():
    """The SSH config file must be correctly configured"""

    ssh_config_ip_addresses = [v.base_container_ip,
                               v.reverse_proxy_ip,
                               v.web_ip,
                               v.db_ip,
                               v.search_ip,
                               v.mirror_ip]

    for ssh_config_ip_address in ssh_config_ip_addresses:
        if ssh_config_ip_address not in open(v.ssh_config).read():
            print("A correctly configured %s file is required\
 to run this application." % (v.ssh_config))

            ssh_config_suggestion = """
You should add the below configuration:

Host %s %s %s %s %s %s
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
  LogLevel=error
""" % (v.base_container_ip,
       v.reverse_proxy_ip,
       v.web_ip,
       v.db_ip,
       v.search_ip,
       v.mirror_ip)

            print(ssh_config_suggestion)
            sys.exit()

check_minimum_python_version()
check_required_executables()
check_minimum_ansible_version()
check_hosts_file()
check_ssh_config_file()
