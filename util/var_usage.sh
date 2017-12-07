#!/usr/bin/env bash

ANSIBLE_VARS="../orchestration/vars.yml"
PREPARE_FILE=$(awk '{print $1}' ${ANSIBLE_VARS} | grep -Ev '(#|^$)' | sed 's/.$//')

arr=(${PREPARE_FILE})
echo ${arr[@]}
