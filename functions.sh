#!/usr/bin/env bash

# Colors
GREEN="\033[0;32m"
RED="\033[0;31m"
BLUE="\033[94m"
COLOR_ENDING="\033[0m"

USER="drucker"

# Networking
NETWORK="drucker"
SUBNET="203.0.113.0/24"
GATEWAY="203.0.113.254"
REVERSE_PROXY_IP="203.0.113.20"
WEB_IP="203.0.113.2"

BASE_IMAGE="debian:latest"
DRUCKER_BASE_IMAGE="drucker:base"
WEB_CONTAINER="drucker_web"
REVERSE_PROXY_CONTAINER="drucker_reverse_proxy"

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

common_ssh_access() {
  # Ensure we have SSH access to the container.
  DEFAULT="$HOME/.ssh/id_rsa.pub"
  read -p "Enter path to SSH public key [${DEFAULT}]: " PUBKEY
  PUBKEY=${PUBKEY:-$DEFAULT}
}

reverse_proxy_ssh_access() {
  common_ssh_access

  cat "${PUBKEY}" > /tmp/authorized_keys
  docker cp /tmp/authorized_keys ${REVERSE_PROXY_CONTAINER}:/home/${USER}/.ssh/authorized_keys
  docker exec -it ${REVERSE_PROXY_CONTAINER} chown -R ${USER}:${USER} /home/${USER}/.ssh
  rm /tmp/authorized_keys
}

reverse_proxy_orchestration() {
  echo -e "${BLUE}Running Reverse Proxy orchestration on the container...${COLOR_ENDING}"
  ansible-playbook -i playbook/hosts playbook/reverse_proxy.yml --user=${USER} --ask-become-pass
}

provision_reverse_proxy_container() {
  if [[ $(docker ps -a \
      | grep -o ${REVERSE_PROXY_CONTAINER}) == "${REVERSE_PROXY_CONTAINER}" ]]; then
    echo -e "${GREEN}${REVERSE_PROXY_CONTAINER} container already exists.${COLOR_ENDING}"

    reverse_proxy_orchestration
  else
    echo -e "${BLUE}Spinning up ${REVERSE_PROXY_CONTAINER} container with ID:${COLOR_ENDING}"

    docker run --name "${REVERSE_PROXY_CONTAINER}" -it \
    --net ${NETWORK} \
    --ip ${REVERSE_PROXY_IP} \
    -d -p 80:80 \
    ${DRUCKER_BASE_IMAGE} bash

    reverse_proxy_ssh_access
    reverse_proxy_orchestration
  fi
}

web_ssh_access() {
  common_ssh_access

  cat "${PUBKEY}" > /tmp/authorized_keys
  docker cp /tmp/authorized_keys ${WEB_CONTAINER}:/home/${USER}/.ssh/authorized_keys
  docker exec -it ${WEB_CONTAINER} chown -R ${USER}:${USER} /home/${USER}/.ssh
  rm /tmp/authorized_keys
}

web_orchestration() {
  echo -e "${BLUE}Running web orchestration on the container...${COLOR_ENDING}"
  ansible-playbook -i playbook/hosts playbook/web.yml --user=${USER} --ask-become-pass
}

provision_web_container() {
  if [[ $(docker ps -a \
      | grep -o ${WEB_CONTAINER}) == "${WEB_CONTAINER}" ]]; then
    echo -e "${GREEN}${WEB_CONTAINER} container already exists.${COLOR_ENDING}"

    web_orchestration
  else
    echo -e "${BLUE}Spinning up ${WEB_CONTAINER} container with ID:${COLOR_ENDING}"

    docker run --name "${WEB_CONTAINER}" -it \
    --net ${NETWORK} \
    --ip ${WEB_IP} \
    -d -p 8080:8080 \
    ${DRUCKER_BASE_IMAGE} bash

    web_ssh_access
    web_orchestration
  fi
}
