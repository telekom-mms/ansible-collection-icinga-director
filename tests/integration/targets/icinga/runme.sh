#!/bin/bash

set -eux

ansible-playbook checkmode.yml --check --diff
ansible-playbook normalmode.yml
