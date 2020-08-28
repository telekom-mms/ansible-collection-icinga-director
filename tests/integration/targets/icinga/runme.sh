#!/usr/bin/env bash

set -eux

ansible-playbook normalmode.yml --diff
ansible-playbook checkmode.yml
ansible-playbook checkmode.yml --check --diff
