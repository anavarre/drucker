FROM debian:stretch

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=drucker
ARG SSH=/home/"$USER"/.ssh

VOLUME ["/data"]

# Ensure we're up-to-date.
RUN apt-get update -y && apt-get upgrade -y

# Make sure dpkg works as intended.
RUN apt-get install -y apt-utils

# Packages needed for Ansible orchestration.
RUN apt-get install -y \
    ssh \
    python-simplejson \
    unzip \
    sudo \
    vim

# Create a drucker sudoer.
RUN adduser -q --disabled-password --gecos '' "$USER" \
    && usermod -aG sudo "$USER"
RUN echo "$USER":"$USER" | chpasswd

# Prepare for SSH access
RUN mkdir -p "$SSH"
ENTRYPOINT service ssh restart && bash
