#!/usr/bin/env bash

# Invoke the script from anywhere (e.g .bashrc alias)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "${DIR}"/functions

export OPTION=$1
export SITENAME=$2

container_files

drucker_argument

check_requirements
configure_ssh_access
create_custom_bridge_network
pull_base_image_from_docker_hub
build_init_image
provision_base_container
provision_reverse_proxy_container
provision_db_container
provision_web_container
allow_web_to_db_ssh_access
provision_search_container
# provision_web2_container has been excluded for now
