#!/usr/bin/env bash

# Invoke the script from anywhere (e.g .bashrc alias)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "${DIR}"/variables
source "${DIR}"/init
source "${DIR}"/ssh
source "${DIR}"/orchestration
source "${DIR}"/containers

check_requirements
ssh_access
create_custom_bridge_network
pull_base_image_from_docker_hub
build_drucker_init_image
provision_base_container
provision_reverse_proxy_container
provision_web_container
