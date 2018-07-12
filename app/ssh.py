#!/usr/bin/env python3
"""Manages SSH access on containers"""

import subprocess as s
import variables as v

TMP_KEY = "/tmp/authorized_keys"

def create_tmp_key():
    """Create temporary SSH key under /tmp"""
    store_key = "cat %s > %s" % (v.DEFAULT_PUBKEY, TMP_KEY)
    s.getoutput(store_key)

def copy_tmp_key(container):
    """Copy temporary SSH key to container"""
    auth_key = "/home/%s/.ssh/authorized_keys" % (v.APP)
    copy_key = "docker cp %s %s:%s" % (TMP_KEY, container, auth_key)
    s.getoutput(copy_key)

def set_ssh_dir_perms(container):
    """Set correct permissions for .ssh directory"""
    chown_ssh = "chown -R %s:%s /home/%s/.ssh" % (v.APP, v.APP, v.APP)
    ssh_dir_perms = "docker exec -it %s %s" % (container, chown_ssh)
    s.getoutput(ssh_dir_perms)

def remove_tmp_key():
    """Remove temporary SSH key"""
    s.getoutput("rm %s" % (TMP_KEY))

def configure_ssh_base():
    """Configure SSH access on base container"""
    create_tmp_key()
    copy_tmp_key(v.BASE_CONTAINER)
    set_ssh_dir_perms(v.BASE_CONTAINER)
    remove_tmp_key()

def configure_ssh_mirror():
    """Configure SSH access on mirror container"""
    create_tmp_key()
    copy_tmp_key(v.MIRROR_CONTAINER)
    set_ssh_dir_perms(v.MIRROR_CONTAINER)
    remove_tmp_key()

def configure_ssh_edge():
    """Configure SSH access on edge container"""
    create_tmp_key()
    copy_tmp_key(v.EDGE_CONTAINER)
    set_ssh_dir_perms(v.EDGE_CONTAINER)
    remove_tmp_key()

def configure_ssh_web():
    """Configure SSH access on web container"""
    create_tmp_key()
    copy_tmp_key(v.WEB_CONTAINER)
    set_ssh_dir_perms(v.WEB_CONTAINER)
    remove_tmp_key()

def configure_ssh_db():
    """Configure SSH access on database container"""
    create_tmp_key()
    copy_tmp_key(v.DB_CONTAINER)
    set_ssh_dir_perms(v.DB_CONTAINER)
    remove_tmp_key()

def configure_ssh_search():
    """Configure SSH access on search container"""
    create_tmp_key()
    copy_tmp_key(v.SEARCH_CONTAINER)
    set_ssh_dir_perms(v.SEARCH_CONTAINER)
    remove_tmp_key()
