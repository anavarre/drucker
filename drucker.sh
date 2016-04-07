#!/usr/bin/env bash

# Invoke the script from anywhere (e.g .bashrc alias)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors
GREEN="\033[0;32m"
RED="\033[0;31m"
BLUE="\033[94m"
COLOR_ENDING="\033[0m"

source ${DIR}/functions.sh

# Set up container.
check_requirements
create_custom_bridge_network
pull_base_image_from_docker_hub
build_drucker_base_image
provision_container
