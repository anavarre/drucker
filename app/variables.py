#!/usr/bin/env python3
import os
from pathlib import Path

app      = "drucker"
app_root = os.path.dirname(os.path.dirname( __file__ ))
app_dir  = app_root + "/app"
home     = str(Path.home())

executables = ["docker", "ansible"]
domains     = "drucker.local phpmyadmin.local adminer.local\
 lightning.local reservoir.local blt.local"
hosts       = "/etc/hosts"

# SSH
ssh_config  = "%s/.ssh/config" % (home)

# IP addresses
base_container_ip = "203.0.113.99"
reverse_proxy_ip  = "203.0.113.2"
web_ip            = "203.0.113.10"
db_ip             = "203.0.113.12"
search_ip         = "203.0.113.13"
mirror_ip         = "203.0.113.50"

# config file
default_config    = app_root + "/config"
default_pubkey    = "%s/.ssh/id_rsa.pub" % (home)
default_html_path = "/var/www/html"
default_db_path   = "/var/lib/mysql"
key_placeholder   = "key_path"
html_placeholder  = "html_path"
db_placeholder    = "db_path"

# Docker networking
subnet        = "203.0.113.0/24"
gateway       = "203.0.113.254"
check_bridge  = "docker network ls | awk '{print $2}' | grep '%s'" % (app)
create_bridge = "docker network create --subnet \"%s\" --gateway \"%s\" \"%s\"" % (subnet, gateway, app)

# Docker images
distro_image        = "debian:stretch"
init_image          = "%s:init" % (app)
base_image          = "%s:base" % (app)
search_image        = "%s:search" % (app)
check_distro_image  = "docker images | awk '{print $1\":\"$2}' | grep \"%s\"" % (distro_image)
check_base_image    = "docker images | awk '{print $1\":\"$2}' | grep \"%s\"" % (base_image)
check_init_image    = "docker images | awk '{print $1\":\"$2}' | grep \"%s\"" % (init_image)
check_search_image  = "docker images | awk '{print $1\":\"$2}' | grep \"%s\"" % (search_image)
update_distro_image = "docker images | awk '{print $1\":\"$2}' | grep \"%s\" | xargs -L1 docker pull" % (distro_image)
pull_distro_image   = "docker pull %s" % (distro_image)
init_image_deletion = "docker rmi \"%s\" > /dev/null 2>&1" % (init_image)

# Docker containers
base_container          = "%s_base" % (app)
check_base_container    = "docker ps -a | grep -o \"%s\"" % (base_container)
create_base_container   = "docker run -d --name %s -it --net %s --ip %s %s bash" % (base_container, app, base_container_ip, init_image)
base_container_deletion = "docker rm -f \"%s\" > /dev/null 2>&1" % (app)
