#!/usr/bin/env python3
import variables as v
import subprocess as s

def configure_base_container_ssh_access():
    """Configure SSH access on base container"""
    tmp_key     = "/tmp/authorized_keys"
    auth_key    = "/home/%s/.ssh/authorized_keys" % (v.app)
    chown_ssh   = "chown -R %s:%s /home/%s/.ssh" % (v.app, v.app, v.app)
    store_key   = "cat %s > %s" % (v.default_pubkey, tmp_key)

    # Create temporary SSH key.
    s.getoutput(store_key)

    # Copy temporary SSH key to host.
    copy_key = "docker cp %s %s:%s" % (tmp_key, v.base_container, auth_key)
    s.getoutput(copy_key)

    # Set correct permissions for .ssh directory.
    ssh_dir_perms = "docker exec -it %s %s" % (v.base_container, chown_ssh)
    s.getoutput(ssh_dir_perms)

    # Remove temporary SSH key.
    s.getoutput("rm %s" % (tmp_key))