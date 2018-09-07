# -*- coding: utf-8 -*-
"""Manages SSH access on containers"""

import subprocess as s
import os
from . import variables as v


TMP_KEY = "/tmp/authorized_keys"


def allow_ssh_access(drucker, host):
    """Allows to set up SSH access from the Web container to any other"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    rsa_drucker_web = "/tmp/id_rsa_drucker_web"
    rsa_key_deployed = "/tmp/rsa_key_deployed"
    key = s.getoutput("cat %s" % (rsa_drucker_web))
    key_check = s.getoutput("cat %s_check" % (rsa_drucker_web))

    if not os.path.isfile(rsa_drucker_web):
        s.run('''docker cp %s:/home/%s/.ssh/id_rsa.pub %s
              ''' % (v.WEB_CONTAINER,
                     v.APP,
                     rsa_drucker_web), shell=True)

        s.run('''docker exec -u %s -it %s /bin/grep -q %s /home/%s/.ssh/authorized_keys > %s
              ''' % (v.APP,
                     host,
                     key,
                     v.APP,
                     rsa_key_deployed), shell=True)

    if not s.getoutput(rsa_key_deployed):
        s.run('''docker exec -u %s -it %s bash -c "echo '%s' >> /home/%s/.ssh/authorized_keys
              ''' % (v.APP,
                     host,
                     key,
                     v.APP), shell=True)
    else:
        s.run('''docker cp %s:/home/%s/.ssh/id_rsa.pub %s_check
              ''' % (v.WEB_CONTAINER,
                     v.APP,
                     rsa_drucker_web), shell=True)

        s.run('''docker exec -u %s -it %s /bin/grep -q %s /home/%s/.ssh/authorized_keys > %s
              ''' % (v.APP,
                     host,
                     key_check,
                     v.APP,
                     rsa_key_deployed), shell=True)

        if (not s.getoutput(rsa_key_deployed) and
                os.path.getsize(s.getoutput(rsa_key_deployed)) != 0):

            s.run('''docker exec -u %s -it %s bash -c "echo '%s' >> /home/%s/.ssh/authorized_keys"
                  ''' % (v.APP,
                         host,
                         key_check,
                         v.APP), shell=True)


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
