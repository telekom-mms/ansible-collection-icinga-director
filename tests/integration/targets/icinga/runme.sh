#!/usr/bin/env bash

set -eux

ansible-playbook normalmode.yml
ansible-playbook checkmode.yml
ansible-playbook checkmode.yml --check --diff
ansible-playbook checkmode_2.yml
ansible-playbook checkmode_2.yml --check --diff
