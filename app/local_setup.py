# -*- coding: utf-8 -*-
"""Edit the config file to accommodate for local user preferences"""

import os
import colorful


def replace_string(file, old_string, new_string):
    """Allows to easily replace a string in a file"""
    with open(file) as target:
        replacement = target.read().replace(old_string, new_string)
    with open(file, "w") as target:
        target.write(replacement)


def set_local_ssh_path(drucker):
    """Write the SSH public key path to the config file"""
    if drucker.vars.KEY_PLACEHOLDER in open(drucker.vars.DEFAULT_CONFIG).read():
        pubkey = input(
            "Enter path to SSH public key (%s): " % (drucker.vars.DEFAULT_PUBKEY)
        )

        if not pubkey:
            replace_string(
                drucker.vars.DEFAULT_CONFIG,
                drucker.vars.KEY_PLACEHOLDER,
                drucker.vars.DEFAULT_PUBKEY,
            )
        elif os.path.isfile(pubkey):
            replace_string(
                drucker.vars.DEFAULT_CONFIG, drucker.vars.KEY_PLACEHOLDER, pubkey
            )
        else:
            print(colorful.red("This filepath doesn't exist. Please try again."))
            set_local_ssh_path(drucker)


def set_local_html_path(drucker):
    """Write the local HTML path to the config file"""
    if drucker.vars.HTML_PLACEHOLDER in open(drucker.vars.DEFAULT_CONFIG).read():
        host_html_path = input(
            """
        Where should we store sites locally? (%s): """
            % (drucker.vars.DEFAULT_HTML_PATH)
        )

        if not host_html_path:
            replace_string(
                drucker.vars.DEFAULT_CONFIG,
                drucker.vars.HTML_PLACEHOLDER,
                drucker.vars.DEFAULT_HTML_PATH,
            )
        elif os.path.isfile(host_html_path):
            replace_string(
                drucker.vars.DEFAULT_CONFIG,
                drucker.vars.HTML_PLACEHOLDER,
                host_html_path,
            )
        else:
            print(colorful.red("This filepath doesn't exist. Please try again."))
            set_local_html_path(drucker)


def set_local_db_path(drucker):
    """Write the local DB path to the config file"""
    if drucker.vars.DB_PLACEHOLDER in open(drucker.vars.DEFAULT_CONFIG).read():
        host_db_path = input(
            """
        Where should we store databases locally? (%s): """
            % (drucker.vars.DEFAULT_DB_PATH)
        )

        if not host_db_path:
            replace_string(
                drucker.vars.DEFAULT_CONFIG,
                drucker.vars.DB_PLACEHOLDER,
                drucker.vars.DEFAULT_DB_PATH,
            )
        elif os.path.isfile(host_db_path):
            replace_string(
                drucker.vars.DEFAULT_CONFIG, drucker.vars.DB_PLACEHOLDER, host_db_path
            )
        else:
            print(colorful.red("This filepath doesn't exist. Please try again."))
            set_local_db_path(drucker)


def main(drucker):
    """Main dispatcher called by the main drucker script."""
    set_local_ssh_path(drucker)
    set_local_html_path(drucker)
    set_local_db_path(drucker)
