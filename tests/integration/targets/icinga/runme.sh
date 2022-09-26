#!/usr/bin/env bash

set -eux

ansible-playbook normalmode.yml -e "@../../integration_config.yml" "$@"
ansible-playbook checkmode.yml -e "@../../integration_config.yml" "$@"
ansible-playbook checkmode.yml -e "@../../integration_config.yml" --check "$@"
ansible-playbook checkmode_2.yml -e "@../../integration_config.yml" "$@"
ansible-playbook checkmode_2.yml -e "@../../integration_config.yml" --check "$@"
