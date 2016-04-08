#!/usr/bin/env bash

# Colors
GREEN="\033[0;32m"
RED="\033[0;31m"
BLUE="\033[94m"
COLOR_ENDING="\033[0m"

# Networking
NETWORK="drucker"
SUBNET="203.0.113.0/24"
GATEWAY="203.0.113.254"
APACHE_IP="203.0.113.2"

BASE_IMAGE="debian:latest"
DRUCKER_BASE_IMAGE="drucker:base"
CONTAINER="drucker_stack"

check_requirements() {
  if [[ -z $(docker --version) ]]; then
    echo "${RED}You need to install Docker before running this script.${COLOR_ENDING}"
    exit 0
  fi

  if [[ -z $(ansible --version) ]]; then
    echo "${RED}You need to install Ansible before running this script.${COLOR_ENDING}"
    exit 0
  fi
}

# Prepare for static IP addresses.
create_custom_bridge_network() {
  if [[ $(docker network ls \
      | awk '{print $2}' \
      | grep ${NETWORK}) ]]; then
    echo -e "${GREEN}Custom ${NETWORK} bridge network already exists.${COLOR_ENDING}"
  else
    echo -e "${BLUE}Creating custom ${NETWORK} bridge network with ID:${COLOR_ENDING}"
    docker network create --subnet ${SUBNET} --gateway ${GATEWAY} ${NETWORK}
  fi
}

pull_base_image_from_docker_hub() {
  if [[ $(docker images \
      | awk '{print $1":"$2}' \
      | grep ${BASE_IMAGE}) ]]; then
    echo -e "${GREEN}${BASE_IMAGE} base image already exists.${COLOR_ENDING}"
    echo -e "${BLUE}Check if ${BASE_IMAGE} can be updated...${COLOR_ENDING}"
      docker images \
      | awk '{print $1":"$2}' \
      | grep ${BASE_IMAGE} \
      | xargs -L1 docker pull
  else
    echo -e "${BLUE}Pulling ${BASE_IMAGE} base image from Docker Hub...${COLOR_ENDING}"
    docker pull ${BASE_IMAGE}
  fi
}

build_drucker_base_image() {
  if [[ $(docker images \
      | awk '{print $1":"$2}' \
      | grep ${DRUCKER_BASE_IMAGE}) ]]; then
    echo -e "${GREEN}${DRUCKER_BASE_IMAGE} custom image already exists.${COLOR_ENDING}"
  else
    echo -e "${BLUE}Building ${DRUCKER_BASE_IMAGE} custom image from Dockerfile...${COLOR_ENDING}"

    docker build -t ${DRUCKER_BASE_IMAGE} .
  fi
}

orchestration() {
  echo -e "${BLUE}Running orchestration on the container...${COLOR_ENDING}"
  ansible-playbook -i playbook/hosts playbook/drucker.yml --user=drucker --ask-become-pass
}

ssh_access() {
  # Ensure we have SSH access to the container.
  DEFAULT="$HOME/.ssh/id_rsa.pub"
  read -p "Enter path to SSH public key [${DEFAULT}]: " PUBKEY
  PUBKEY=${PUBKEY:-$DEFAULT}

  cat "${PUBKEY}" > /tmp/authorized_keys
  docker cp /tmp/authorized_keys ${CONTAINER}:/home/drucker/.ssh/authorized_keys
  docker exec -it ${CONTAINER} chown -R drucker:drucker /home/drucker/.ssh
  rm /tmp/authorized_keys
}

provision_container() {
  if [[ $(docker ps -a \
      | grep -o ${CONTAINER}) == "${CONTAINER}" ]]; then
    echo -e "${GREEN}${CONTAINER} container already exists.${COLOR_ENDING}"

    orchestration
  else
    echo -e "${BLUE}Spinning up ${CONTAINER} container with ID:${COLOR_ENDING}"

    docker run --name "${CONTAINER}" -it \
    --net ${NETWORK} \
    --ip ${APACHE_IP} \
    -d -p 80:80 \
    ${DRUCKER_BASE_IMAGE} bash

    ssh_access
    orchestration
  fi
}
