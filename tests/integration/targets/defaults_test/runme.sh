#!/usr/bin/env bash

set -eux

ansible-playbook defaults_test.yml -e "@../../integration_config.yml" "$@"
