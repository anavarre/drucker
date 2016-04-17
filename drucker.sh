#!/usr/bin/env bash

# Invoke the script from anywhere (e.g .bashrc alias)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "${DIR}"/containers/variables
source "${DIR}"/containers/init
source "${DIR}"/containers/ssh
source "${DIR}"/containers/orchestration
source "${DIR}"/containers/base
source "${DIR}"/containers/reverse_proxy
source "${DIR}"/containers/web
source "${DIR}"/containers/gluster

check_requirements
configure_ssh_access
create_custom_bridge_network
pull_base_image_from_docker_hub
build_init_image
provision_base_container
provision_reverse_proxy_container
provision_web_container
provision_gluster_container
