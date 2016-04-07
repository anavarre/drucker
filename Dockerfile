FROM debian:latest

ENV DEBIAN_FRONTEND noninteractive
ENV USER drucker
ENV SSH /home/$USER/.ssh

RUN apt-get update -y && apt-get upgrade -y

# Packages needed for Ansible orchestration.
RUN apt-get install -y \
ssh \
python-simplejson \
unzip \
sudo

# Create a drucker sudoer.
RUN adduser -q --disabled-password --gecos '' $USER \
&& usermod -aG sudo $USER
RUN echo "$USER:$USER" | chpasswd

RUN mkdir -p $SSH

ENTRYPOINT service ssh restart && bash
