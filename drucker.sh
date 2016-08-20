#!/usr/bin/env bash

# Invoke the script from anywhere (e.g .bashrc alias)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

usage() {
  FIRST_ARG=$1

  if [[ "$FIRST_ARG" == "--help" ]]; then
cat <<EOF
--dev     Prepare drucker for development work with no caching and helper modules enabled. WARNING: when running automated tests, 'twig_debug'
should be set to FALSE.
--prod    Opinionated setup with all known performance best practices enabled.
EOF
    exit 0
  elif [[ -n "${FIRST_ARG}" ]] && [[ "${FIRST_ARG}" != "--dev" ]] && [[ "${FIRST_ARG}" != "--prod" ]]; then
    echo "Usage: drucker {--dev|--prod}"
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
# provision_web2_container has been excluded for now
