#!/usr/bin/env bash

# Invoke the script from anywhere (e.g .bashrc alias)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "${DIR}/init"
load_function_files
load_container_files

$(command -v python3) app/requirements.py

source "${DIR}/config"

export COMMAND=$1
export SITENAME=$2

# Force lowercase on sitename(s).
export SITENAME=$(echo "$SITENAME" | tr '[:upper:]' '[:lower:]')

if [[ $3 = *.* ]]; then
  export GIT_TAG=$3
fi

# Custom user configuration.
$(command -v python3) app/local_setup.py

# Are we running drucker with a CLI argument?
drucker_argument

# drucker initialization.
create_custom_bridge_network
pull_base_image_from_docker_hub
build_init_image
# Container provisioning and orchestration.
provision_base_container
provision_mirror_container
provision_reverse_proxy_container
provision_db_container
provision_search_container
provision_web_container
allow_web_to_db_ssh_access
