# -*- coding: utf-8 -*-
"""Edit the config file to accommodate for local user preferences"""

import os
import colorful as c
from . import variables as v


def replace_string(file, old_string, new_string):
    """Allows to easily replace a string in a file"""
    with open(file) as target:
        replacement = target.read().replace(old_string, new_string)
    with open(file, "w") as target:
        target.write(replacement)


def set_local_ssh_path():
    """Write the SSH public key path to the config file"""
    if v.KEY_PLACEHOLDER in open(v.DEFAULT_CONFIG).read():
        pubkey = input("Enter path to SSH public key (%s): " % (v.DEFAULT_PUBKEY))

        if not pubkey:
            replace_string(v.DEFAULT_CONFIG, v.KEY_PLACEHOLDER, v.DEFAULT_PUBKEY)
        elif os.path.isfile(pubkey):
            replace_string(v.DEFAULT_CONFIG, v.KEY_PLACEHOLDER, pubkey)
        else:
            print(c.red("This filepath doesn't exist. Please try again."))
            set_local_ssh_path()


def set_local_html_path():
    """Write the local HTML path to the config file"""
    if v.HTML_PLACEHOLDER in open(v.DEFAULT_CONFIG).read():
        host_html_path = input('''
        Where should we store sites locally? (%s): ''' % (v.DEFAULT_HTML_PATH))

        if not host_html_path:
            replace_string(v.DEFAULT_CONFIG, v.HTML_PLACEHOLDER, v.DEFAULT_HTML_PATH)
        elif os.path.isfile(host_html_path):
            replace_string(v.DEFAULT_CONFIG, v.HTML_PLACEHOLDER, host_html_path)
        else:
            print(c.red("This filepath doesn't exist. Please try again."))
            set_local_html_path()


def set_local_db_path():
    """Write the local DB path to the config file"""
    if v.DB_PLACEHOLDER in open(v.DEFAULT_CONFIG).read():
        host_db_path = input('''
        Where should we store databases locally? (%s): ''' % (v.DEFAULT_DB_PATH))

        if not host_db_path:
            replace_string(v.DEFAULT_CONFIG, v.DB_PLACEHOLDER, v.DEFAULT_DB_PATH)
        elif os.path.isfile(host_db_path):
            replace_string(v.DEFAULT_CONFIG, v.DB_PLACEHOLDER, host_db_path)
        else:
            print(c.red("This filepath doesn't exist. Please try again."))
            set_local_db_path()


def main():
    """Main dispatcher called by the main drucker script."""
    set_local_ssh_path()
    set_local_html_path()
    set_local_db_path()
