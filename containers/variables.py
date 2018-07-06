#!/usr/bin/env python
from pathlib import Path

home = str(Path.home())

executables = ["docker", "ansible"]
domains     = "drucker.local phpmyadmin.local adminer.local\
 lightning.local reservoir.local blt.local"
hosts       = "/etc/hosts"
ssh_config  = "%s/.ssh/config" % (home)

# IP addresses
base_container_ip = "203.0.113.99"
reverse_proxy_ip  = "203.0.113.2"
web_ip            = "203.0.113.10"
db_ip             = "203.0.113.12"
search_ip         = "203.0.113.13"
mirror_ip         = "203.0.113.50"
