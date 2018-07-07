#!/usr/bin/env python
import os
from pathlib import Path

home = str(Path.home())

executables = ["docker", "ansible"]
domains     = "drucker.local phpmyadmin.local adminer.local\
 lightning.local reservoir.local blt.local"
hosts       = "/etc/hosts"
ssh_config  = "%s/.ssh/config" % (home)

# config file
default_config    = os.getcwd() + "/config"
default_pubkey    = "%s/.ssh/id_rsa.pub" % (home)
default_html_path = "/var/www/html"
default_db_path   = "/var/lib/mysql"
key_placeholder   = "key_path"
html_placeholder  = "html_path"
db_placeholder    = "db_path"

# IP addresses
base_container_ip = "203.0.113.99"
reverse_proxy_ip  = "203.0.113.2"
web_ip            = "203.0.113.10"
db_ip             = "203.0.113.12"
search_ip         = "203.0.113.13"
mirror_ip         = "203.0.113.50"
