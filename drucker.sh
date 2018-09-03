#!/usr/bin/env bash

# Invoke the script from anywhere (e.g .bashrc alias)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

APP="`command -v python3` ${DIR}/app"

# Make sure the app can run successfully.
${APP}/requirements.py
${APP}/local_setup.py

# Are we running drucker with a CLI argument?
if [[ $# -eq 1 ]]; then
  export COMMAND=$1
  ${APP}/arguments.py ${COMMAND}
  exit 1
elif [[ $# -eq 2 ]]; then
  export COMMAND=$1
  export SITENAME=$2
  ${APP}/arguments.py ${COMMAND} ${SITENAME}
  exit 1
fi

# source "${DIR}/init"
# load_function_files
# load_container_files

# source "${DIR}/config"

# Force lowercase on sitename(s).
# export SITENAME=$(echo "$SITENAME" | tr '[:upper:]' '[:lower:]')

# if [[ $3 = *.* ]]; then
#   export GIT_TAG=$3
# fi

#$(command -v python3) ${DIR}/app/ssh.py

# Are we running drucker with a CLI argument?
# drucker_argument

# # drucker initialization.
${APP}/init.py
# Container provisioning and orchestration.
${APP}/base.py
${APP}/mirror.py
${APP}/edge.py
${APP}/db.py
${APP}/search.py
${APP}/web.py
