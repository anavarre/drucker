# -*- coding: utf-8 -*-
"""Manages SSH access on containers"""

import os
import subprocess


TMP_KEY = "/tmp/authorized_keys"


def allow_ssh_access(drucker, host):
    """Allows to set up SSH access from the Web container to any other"""
    assert drucker  # TODO: Remove after porting this to use drucker object.
    rsa_drucker_web = "/tmp/id_rsa_drucker_web"
    rsa_key_deployed = "/tmp/rsa_key_deployed"
    key = subprocess.getoutput("cat %s" % (rsa_drucker_web))
    key_check = subprocess.getoutput("cat %s_check" % (rsa_drucker_web))

    if not os.path.isfile(rsa_drucker_web):
        subprocess.run("docker cp %s:/home/%s/.ssh/id_rsa.pub %s"
                       % (drucker.vars.WEB_CONTAINER,
                          drucker.vars.APP,
                          rsa_drucker_web), shell=True)

        subprocess.run("docker exec -u %s -it %s /bin/grep -q %s /home/%s/.ssh/authorized_keys > %s"
                       % (drucker.vars.APP,
                          host,
                          key,
                          drucker.vars.APP,
                          rsa_key_deployed),
                          shell=True)

    if not subprocess.getoutput(rsa_key_deployed):
        subprocess.run('''docker exec -u %s -it %s bash -c "echo '%s' >> /home/%s/.ssh/authorized_keys
                       ''' % (drucker.vars.APP,
                          host,
                          key,
                          drucker.vars.APP),
                          shell=True)
    else:
        subprocess.run("docker cp %s:/home/%s/.ssh/id_rsa.pub %s_check"
                       % (drucker.vars.WEB_CONTAINER,
                          drucker.vars.APP,
                          rsa_drucker_web), shell=True)

        subprocess.run("docker exec -u %s -it %s /bin/grep -q %s /home/%s/.ssh/authorized_keys > %s"
                       % (drucker.vars.APP,
                          host,
                          key_check,
                          drucker.vars.APP,
                          rsa_key_deployed), shell=True)

        if (not subprocess.getoutput(rsa_key_deployed) and
                os.path.getsize(subprocess.getoutput(rsa_key_deployed)) != 0):

            subprocess.run('''docker exec -u %s -it %s bash -c "echo '%s' >> /home/%s/.ssh/authorized_keys"
                           '''  % (drucker.vars.APP,
                                   host,
                                   key_check,
                                   drucker.vars.APP), shell=True)


def create_tmp_key():
    """Create temporary SSH key under /tmp"""
    store_key = "cat %s > %s" % (drucker.vars.DEFAULT_PUBKEY, TMP_KEY)
    subprocess.getoutput(store_key)


def copy_tmp_key(container):
    """Copy temporary SSH key to container"""
    auth_key = "/home/%s/.ssh/authorized_keys" % (drucker.vars.APP)
    copy_key = "docker cp %s %s:%s" % (TMP_KEY, container, auth_key)
    subprocess.getoutput(copy_key)


def set_ssh_dir_perms(container):
    """Set correct permissions for .ssh directory"""
    chown_ssh = "chown -R %s:%s /home/%s/.ssh" % (drucker.vars.APP, drucker.vars.APP, drucker.vars.APP)
    ssh_dir_perms = "docker exec -it %s %s" % (container, chown_ssh)
    subprocess.getoutput(ssh_dir_perms)


def remove_tmp_key():
    """Remove temporary SSH key"""
    subprocess.getoutput("rm %s" % (TMP_KEY))


def configure_ssh_base():
    """Configure SSH access on base container"""
    create_tmp_key()
    copy_tmp_key(drucker.vars.BASE_CONTAINER)
    set_ssh_dir_perms(drucker.vars.BASE_CONTAINER)
    remove_tmp_key()


def configure_ssh_mirror():
    """Configure SSH access on mirror container"""
    create_tmp_key()
    copy_tmp_key(drucker.vars.MIRROR_CONTAINER)
    set_ssh_dir_perms(drucker.vars.MIRROR_CONTAINER)
    remove_tmp_key()


def configure_ssh_edge():
    """Configure SSH access on edge container"""
    create_tmp_key()
    copy_tmp_key(drucker.vars.EDGE_CONTAINER)
    set_ssh_dir_perms(drucker.vars.EDGE_CONTAINER)
    remove_tmp_key()


def configure_ssh_web():
    """Configure SSH access on web container"""
    create_tmp_key()
    copy_tmp_key(drucker.vars.WEB_CONTAINER)
    set_ssh_dir_perms(drucker.vars.WEB_CONTAINER)
    remove_tmp_key()


def configure_ssh_db():
    """Configure SSH access on database container"""
    create_tmp_key()
    copy_tmp_key(drucker.vars.DB_CONTAINER)
    set_ssh_dir_perms(drucker.vars.DB_CONTAINER)
    remove_tmp_key()


def configure_ssh_search():
    """Configure SSH access on search container"""
    create_tmp_key()
    copy_tmp_key(drucker.vars.SEARCH_CONTAINER)
    set_ssh_dir_perms(drucker.vars.SEARCH_CONTAINER)
    remove_tmp_key()
