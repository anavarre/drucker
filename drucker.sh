#!/usr/bin/env bash

# Invoke the script from anywhere (e.g .bashrc alias)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "${DIR}/init"
load_function_files
load_container_files

$(command -v python3) ${DIR}/app/requirements.py

source "${DIR}/config"

export COMMAND=$1
export SITENAME=$2

# Force lowercase on sitename(s).
export SITENAME=$(echo "$SITENAME" | tr '[:upper:]' '[:lower:]')

if [[ $3 = *.* ]]; then
  export GIT_TAG=$3
fi

# Custom user configuration.
$(command -v python3) ${DIR}/app/local_setup.py


#$(command -v python3) ${DIR}/app/ssh.py


# Are we running drucker with a CLI argument?
drucker_argument

# # drucker initialization.
$(command -v python3) ${DIR}/app/init.py

# Container provisioning and orchestration.
$(command -v python3) ${DIR}/app/base.py
$(command -v python3) ${DIR}/app/mirror.py
$(command -v python3) ${DIR}/app/edge.py
$(command -v python3) ${DIR}/app/db.py
$(command -v python3) ${DIR}/app/search.py
# provision_web_container
# allow_web_to_db_ssh_access
