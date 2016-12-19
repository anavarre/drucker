#!/usr/bin/env bash

# Invoke the script from anywhere (e.g .bashrc alias)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# shellcheck source=/dev/null
source "${DIR}/config"
# shellcheck source=/dev/null
source "${DIR}/functions"

export OPTION=$1
export SITENAME=$2

# Custom user configuration.
set_local_ssh_path
set_local_html_path
set_local_db_path

load_container_files

# Are we running drucker with a CLI argument?
drucker_argument

check_requirements

# drucker initialization.
create_custom_bridge_network
pull_base_image_from_docker_hub
build_init_image
# Container provisioning and orchestration.
provision_base_container
provision_reverse_proxy_container
provision_db_container
provision_search_container
provision_web_container
allow_web_to_db_ssh_access
# provision_web2_container has been excluded for now
