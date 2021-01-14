#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 T-Systems Multimedia Solutions GmbH
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: icinga_host_template
short_description: Manage host templates in Icinga2
description:
   - Add or remove a host template to Icinga2 through the director API.
author: Michaela Mattes (@michaelamattes)
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
version_added: '1.2.0'
notes:
  - This module supports check mode.
options:
  state:
    description:
      - Apply feature state.
    choices: [ "present", "absent" ]
    default: present
    type: str
  object_name:
    description:
      - Icinga object name for this host template.
      - This is usually a fully qualified host name but it could basically be any kind of string.
      - To make things easier for your users we strongly suggest to use meaningful names for templates.
      - For example "generic-host" is ugly, "Standard Linux Server" is easier to understand.
    aliases: ['name']
    required: true
    type: str
  display_name:
    description:
      - Alternative name for this host.
      - Might be a host alias or and kind of string helping your users to identify this host.
    type: str
  address:
    description:
      - Host address. Usually an IPv4 address, but may be any kind of address your check plugin is able to deal with.
    type: str
  address6:
    description:
      - Host IPv6 address. Usually an IPv64 address, but may be any kind of address your check plugin is able to deal with.
    type: str
  groups:
    description:
      - Hostgroups that should be directly assigned to this node. Hostgroups can be useful for various reasons.
      - You might assign service checks based on assigned hostgroup. They are also often used as an instrument to enforce restricted views in Icinga Web 2.
      - Hostgroups can be directly assigned to single hosts or to host templates.
      - You might also want to consider assigning hostgroups using apply rules.
    type: list
    elements: str
    default: []
  check_command:
    description:
      - The name of the check command.
      - Though this is not required to be defined in the director, you still have to supply a check_command in a host or host-template.
    type: str
  check_interval:
    description:
      - Your regular check interval.
    type: str
  disabled:
    description:
      - Disabled objects will not be deployed.
    default: False
    type: bool
    choices: [True, False]
  imports:
    description:
      - Choose a host-template.
    type: list
    elements: str
  zone:
    description:
      - Set the zone.
    type: str
  vars:
    description:
      - Custom properties of the host.
    type: "dict"
  notes:
    description:
      - Additional notes for this object.
    type: str
    version_added: '1.8.0'
  notes_url:
    description:
      - An URL pointing to additional notes for this object.
      - Separate multiple urls like this "'http://url1' 'http://url2'".
      - Maximum length is 255 characters.
    type: str
    version_added: '1.8.0'
  has_agent:
    description:
      - Whether this host has the Icinga 2 Agent installed.
    type: bool
    choices: [True, False]
    version_added: '1.9.0'
  master_should_connect:
    description:
      - Whether the parent (master) node should actively try to connect to this agent.
    type: bool
    choices: [True, False]
    version_added: '1.9.0'
  accept_config:
    description:
      - Whether the agent is configured to accept config.
    type: bool
    choices: [True, False]
    version_added: '1.9.0'
"""

EXAMPLES = """
- name: Create host template
  t_systems_mms.icinga_director.icinga_host_template:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: foohosttemplate
    display_name: foohosttemplate
    disabled: false
    check_command: dummy
    check_interval: 90s
    groups:
      - "foohostgroup"
    imports:
      - ''
    notes: "example note"
    notes_url: "'http://url1' 'http://url2'"
    has_agent: true
    master_should_connect: true
    accept_config: true
"""

RETURN = r""" # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec
from ansible_collections.t_systems_mms.icinga_director.plugins.module_utils.icinga import (
    Icinga2APIObject,
)


# ===========================================
# Module execution.
#
def main():
    # use the predefined argument spec for url
    argument_spec = url_argument_spec()
    # add our own arguments
    argument_spec.update(
        state=dict(default="present", choices=["absent", "present"]),
        url=dict(required=True),
        object_name=dict(required=True, aliases=["name"]),
        display_name=dict(required=False),
        groups=dict(type="list", elements="str", default=[], required=False),
        check_command=dict(required=False),
        check_interval=dict(required=False),
        imports=dict(type="list", elements="str", required=False),
        disabled=dict(type="bool", default=False, choices=[True, False]),
        address=dict(required=False),
        address6=dict(required=False),
        zone=dict(required=False, default=None),
        vars=dict(type="dict", default=None),
        notes=dict(type="str", required=False),
        notes_url=dict(type="str", required=False),
        has_agent=dict(type="bool", choices=[True, False]),
        master_should_connect=dict(type="bool", choices=[True, False]),
        accept_config=dict(type="bool", choices=[True, False]),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    data = {
        "object_name": module.params["object_name"],
        "object_type": "template",
        "display_name": module.params["display_name"],
        "groups": module.params["groups"],
        "check_command": module.params["check_command"],
        "check_interval": module.params["check_interval"],
        "imports": module.params["imports"],
        "disabled": module.params["disabled"],
        "address": module.params["address"],
        "address6": module.params["address6"],
        "zone": module.params["zone"],
        "vars": module.params["vars"],
        "notes": module.params["notes"],
        "notes_url": module.params["notes_url"],
        "has_agent": module.params["has_agent"],
        "master_should_connect": module.params["master_should_connect"],
        "accept_config": module.params["accept_config"],
    }

    icinga_object = Icinga2APIObject(module=module, path="/host", data=data)

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
