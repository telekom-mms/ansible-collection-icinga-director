#!/usr/bin/env bash

set -eux

ansible-playbook normalmode.yml -e "@../../integration_config.yml" --check "$@"
ansible-playbook normalmode.yml -e "@../../integration_config.yml" "$@"
