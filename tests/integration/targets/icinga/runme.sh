#!/usr/bin/env bash

set -eux

ansible-playbook normalmode.yml -v --diff
ansible-playbook checkmode.yml -v --diff
ansible-playbook checkmode.yml --check --diff -v
ansible-playbook checkmode_2.yml -v --diff
ansible-playbook checkmode_2.yml --check --diff -v
