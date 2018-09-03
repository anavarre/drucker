#!/usr/bin/env python3
"""Common variables used across the app"""

import os
from pathlib import Path

APP = "drucker"
APP_VERSION="dev"
APP_ROOT = os.path.dirname(os.path.dirname(__file__))
APP_DIR = "%s/app" % (APP_ROOT)
HOME = str(Path.home())

EXECUTABLES = ["docker", "ansible"]
DOMAINS = "drucker.local phpmyadmin.local adminer.local\
 lightning.local reservoir.local blt.local"
HOSTS = "/etc/hosts"
TEST_GROUPS = ["system", "mirror", "edge", "db", "search", "web"]

# SSH
SSH_CONFIG = "%s/.ssh/config" % (HOME)

# IP addresses
BASE_IP = "203.0.113.99"
MIRROR_IP = "203.0.113.50"
EDGE_IP = "203.0.113.2"
DB_IP = "203.0.113.12"
WEB_IP = "203.0.113.10"
SEARCH_IP = "203.0.113.13"

# config file
DEFAULT_CONFIG = APP_ROOT + "/config"
DEFAULT_PUBKEY = "%s/.ssh/id_rsa.pub" % (HOME)
DEFAULT_HTML_PATH = "/var/www/html"
DEFAULT_DB_PATH = "/var/lib/mysql"
KEY_PLACEHOLDER = "key_path"
HTML_PLACEHOLDER = "html_path"
DB_PLACEHOLDER = "db_path"

# Docker networking
SUBNET = "203.0.113.0/24"
GATEWAY = "203.0.113.254"
CHECK_BRIDGE = "docker network ls | awk '{print $2}' | grep '%s'" % (APP)
CREATE_BRIDGE = '''
docker network create --subnet \"%s\" --gateway \"%s\" \"%s\"
''' % (SUBNET, GATEWAY, APP)

# Docker images
DISTRO_IMAGE = "debian:stretch"
INIT_IMAGE = "%s:init" % (APP)
BASE_IMAGE = "%s:base" % (APP)
MIRROR_IMAGE = "%s:mirror" % (APP)
EDGE_IMAGE = "%s:edge" % (APP)
DB_IMAGE = "%s:db" % (APP)
WEB_IMAGE = "%s:web" % (APP)
SEARCH_IMAGE = "%s:search" % (APP)
CHECK_DISTRO_IMAGE = "docker images | awk '{print $1\":\"$2}' | grep \"%s\"" % (DISTRO_IMAGE)
CHECK_INIT_IMAGE = "docker images | awk '{print $1\":\"$2}' | grep %s" % (INIT_IMAGE)
CHECK_BASE_IMAGE = "docker images | awk '{print $1\":\"$2}' | grep %s" % (BASE_IMAGE)
CHECK_SEARCH_IMAGE = "docker images | awk '{print $1\":\"$2}' | grep \"%s\"" % (SEARCH_IMAGE)
UPDATE_DISTRO_IMAGE = '''
docker images | awk '{print $1\":\"$2}' | grep \"%s\" | xargs -L1 docker pull
''' % (DISTRO_IMAGE)
PULL_DISTRO_IMAGE = "docker pull %s" % (DISTRO_IMAGE)

# Docker containers
BASE_CONTAINER = "%s_base" % (APP)
MIRROR_CONTAINER = "%s_mirror" % (APP)
EDGE_CONTAINER = "%s_edge" % (APP)
DB_CONTAINER = "%s_db" % (APP)
WEB_CONTAINER = "%s_web" % (APP)
SEARCH_CONTAINER = "%s_search" % (APP)

CONTAINERS= [MIRROR_CONTAINER,
             EDGE_CONTAINER,
             DB_CONTAINER,
             WEB_CONTAINER,
             SEARCH_CONTAINER]

# Hostnames
TLD = "local"
MIRROR_HOSTNAME = "mirror.%s" % (TLD)
EDGE_HOSTNAME = "edge.%s" % (TLD)
WEB_HOSTNAME = "web.%s" % (TLD)
DB_HOSTNAME = "db.%s" % (TLD)
SEARCH_HOSTNAME = "search.%s" % (TLD)

# Ports
HOST_EDGE_PORT = "81"
MIRROR_PORT = "3142"
EDGE_PORT = "80"
HOST_WEB_PORT = "8180"
HOST_DB_PORT = "3307"
HOST_SEARCH_PORT = "8984"
WEB_PORT = "8080"
DB_PORT = "3306"
SEARCH_PORT = "8983"
HOST_TCP_PORT_MAPPER_WEB = "2047"
TCP_PORT_MAPPER_WEB = "2049"
HOST_TCP_PORT_MAPPER_DB = "2051"
TCP_PORT_MAPPER_DB = "2052"

# Volume mappings
CONTAINER_DB_PATH = "/var/lib/mysql"
CONTAINER_HTML_PATH = "/var/www/html"
CONTAINER_IMPORT_PATH = "%s/import" % (CONTAINER_HTML_PATH)
HOST_HTML_PATH = CONTAINER_HTML_PATH

# Services
DEFAULT_PHP = "7.2"
PREVIOUS_PHP = "7.1"

# Database
MYSQL_DIR_OWNERSHIP = "mysql"