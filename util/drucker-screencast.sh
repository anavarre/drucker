#!/usr/bin/env bash

# Run:
#   $ clear ; asciinema rec -t "drucker" -w 2 /tmp/drucker.json
# Then, immediately after:
#   $ ./drucker-screencast.sh
# To upload the screencast, type:
#   $ asciinema upload /tmp/drucker.json

function recorder_check() {
  RECORDER="$(which asciinema)"

  if [[ ! ${RECORDER} ]]; then
    echo 'asciinema must be installed to run this script.'
    exit 0
  fi
}

recorder_check

function wait() {
  sleep 2
  echo ---------------------------------------------
  sleep 3
}

function separator() {
  echo -e "\n"
  sleep 2
}

clear

echo "*******************************************"
echo "*                                         *"
echo "* This is a quick introduction to drucker *"
echo "* https://github.com/anavarre/drucker     *"
echo "*                                         *"
echo "*******************************************"

sleep 2

separator
echo "First, let's get confirmation we meet the
minimum software requirements."

wait

docker --version |\
  awk '{print $3}' |\
  cut -c -6 |\
  xargs echo Docker version:

ansible --version |\
  awk '{print $2}' |\
  xargs echo Ansible version: |\
  cut -c -24 ;

separator

echo "Now we can check both our Docker images and
corresponding containers are alive and well."

wait

docker ps --format 'table {{.Names}}\t{{.Image}}'

separator
echo "Next up, we want to ensure our hosts file is
correctly configured."

wait

tail -n3 /etc/hosts

separator
echo "To make sure SSH access will be working, we
also need to confirm our config file exists"

wait

cat ~/.ssh/config

separator
echo ">>>> You can find all of the above in the README.md file."

separator
echo "Okay. Now, let's explore what drucker has to
offer. Type 'drucker help'"

wait

"$HOME/Sites/git/github/drucker/drucker" --help

separator

echo "Assumptions are being made both with the 'dev'
and 'prod' modes. Just type 'drucker' if you wish
to go with the defaults only."

wait
separator

echo "Let's go ahead and run drucker!"

wait

"$HOME/Sites/git/github/drucker/drucker"

separator
echo "That was pretty fast, right? This is because
both the images and containers already exist.
It'll take a good 10-15mn on average broadband
when you run it for the first time."

separator
sleep 2
echo "OK. Now let's check the headers."

wait

http -h drucker.local | egrep '(X-Generator:|Server:|Via:)'

separator
echo "Excellent. We're running Drupal 8 behind
Varnish and nginx. Non-cacheable requests will be
sent to the Apache backend as with a normal stack."

separator
echo "This is drucker in a nutshell. Hope you like it.
Thanks for watching!"
