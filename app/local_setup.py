#!/usr/bin/env python
"""Edit the config file to accommodate for local user preferences"""
import variables as v

def replace_string(file, old_string, new_string):
    """Allows to easily replace a string in a file"""
    with open(file) as f:
        replacement = f.read().replace(old_string, new_string)
    with open(file, "w") as f:
        f.write(replacement)

def set_local_ssh_path():
    """Write the SSH public key path to the config file"""
    if v.key_placeholder in open(v.default_config).read():
        pubkey = input("Enter path to SSH public key (%s): " % (v.default_pubkey))

        if not pubkey:
            replace_string(v.default_config, v.key_placeholder, v.default_pubkey)
        elif os.path.isfile(pubkey):
            replace_string(v.default_config, v.key_placeholder, pubkey)
        else:
            print("This filepath doesn't exist. Please try again.")
            set_local_ssh_path()

def set_local_html_path():
    """Write the local HTML path to the config file"""
    if v.html_placeholder in open(v.default_config).read():
        host_html_path = input("Where should we store sites locally? (%s): " % (v.default_html_path))

        if not host_html_path:
            replace_string(v.default_config, v.html_placeholder, v.default_html_path)
        elif os.path.isfile(host_html_path):
            replace_string(v.default_config, v.html_placeholder, host_html_path)
        else:
            print("This filepath doesn't exist. Please try again.")
            set_local_html_path()

def set_local_db_path():
    """Write the local DB path to the config file"""
    if v.db_placeholder in open(v.default_config).read():
        host_db_path = input("Where should we store databases locally? (%s): " % (v.default_db_path))

        if not host_db_path:
            replace_string(v.default_config, v.db_placeholder, v.default_db_path)
        elif os.path.isfile(host_db_path):
            replace_string(v.default_config, v.db_placeholder, host_db_path)
        else:
            print("This filepath doesn't exist. Please try again.")
            set_local_db_path()

set_local_ssh_path()
set_local_html_path()
set_local_db_path()
