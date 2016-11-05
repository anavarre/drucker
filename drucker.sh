#!/usr/bin/env bash

# Invoke the script from anywhere (e.g .bashrc alias)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

usage() {
  export OPTION=$1
  export SITENAME=$2

  if [[ "$OPTION" == "--help" ]]; then
cat <<EOF
--dev                 Prepare drucker for development work with no caching and helper modules enabled.
                      WARNING: when running automated tests, 'twig_debug' should be set to FALSE.

--prod                Opinionated setup with all known performance best practices enabled.

--reinstall           Deletes the existing drucker codebase and database and reinstalls from the latest dev tarball.

--delete [sitename]   Deletes an arbitrary docroot, vHost and corresponding database.

--import [sitename]   Imports the database, files and codebase from the import directory.
EOF
    exit 0
  elif [[ -n "${OPTION}" ]] && \
       [[ "${OPTION}" != "--dev" ]] && \
       [[ "${OPTION}" != "--prod" ]] && \
       [[ "${OPTION}" != "--reinstall" ]] && \
       [[ "${OPTION}" != "--delete" ]] && \
       [[ "${OPTION}" != "--import" ]]; then
    echo "Usage: drucker {--dev|--prod|--reinstall|--delete [sitename]|--import [sitename]}"
    exit 0
  elif [[ "${OPTION}" == "--import" ]] && [[ -z ${2} ]]; then
    echo "Usage: drucker {--dev|--prod|--reinstall|--delete [sitename]|--import [sitename]}"
    exit 0
  fi
}

usage "$@"

CONTAINER_DIR="containers"
CONTAINER_FILES="variables init ssh orchestration base reverse_proxy web db"
# web2 has been excluded for now

for FILES in ${CONTAINER_FILES} ; do
  source "${DIR}/${CONTAINER_DIR}/${FILES}"
done

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
# provision_web2_container has been excluded for now
