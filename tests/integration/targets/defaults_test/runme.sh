#!/usr/bin/env bash

set -eux

ansible-playbook defaults_test.yml -v --diff
