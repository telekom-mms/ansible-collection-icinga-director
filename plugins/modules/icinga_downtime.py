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
module: icinga_host
short_description: Manage hosts in Icinga2
description:
   - Add or remove a host to Icinga2 through the director API.
author: Sebastian Gumprich (@rndmh3ro)
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
version_added: '1.0.0'
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
      - Icinga object name for this host.
      - This is usually a fully qualified host name but it could basically be any kind of string.
      - To make things easier for your users we strongly suggest to use meaningful names for templates.
      - For example "generic-host" is ugly, "Standard Linux Server" is easier to understand.
    aliases: ['name']
    required: true
    type: str
  display_name:
    description:
      - Alternative name for this host.
        Might be a host alias or and kind of string helping your users to identify this host.
    type: str
  address:
    description:
      - Host address. Usually an IPv4 address, but may be any kind of address your check plugin is able to deal with.
    type: str
  address6:
    description:
      - Host IPv6 address. Usually an IPv6 address, but may be any kind of address your check plugin is able to deal with.
    type: str
    version_added: '1.4.0'
  groups:
    description:
      - Hostgroups that should be directly assigned to this node. Hostgroups can be useful for various reasons.
      - You might assign service checks based on assigned hostgroup. They are also often used as an instrument to
        enforce restricted views in Icinga Web 2.
      - Hostgroups can be directly assigned to single hosts or to host templates.
      - You might also want to consider assigning hostgroups using apply rules.
    type: list
    elements: str
    default: []
  disabled:
    description:
      - Disabled objects will not be deployed.
    default: False
    type: bool
    choices: [True, False]
  imports:
    description:
      - Choose a Host Template. Required when state is C(present).
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
  check_command:
    description:
      - The name of the check command.
      - Though this is not required to be defined in the director, you still have to supply a check_command in a host or host-template.
    type: str
  notes:
    description:
      - Additional notes for this object.
    type: str
    version_added: '1.8.0'
  notes_url:
    description:
      - An URL pointing to additional notes for this object.
      - Separate multiple urls like this "'http://url1' 'http://url2'".
      - The maximum length is 255 characters.
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
  command_endpoint:
    description:
      - The endpoint where commands are executed on.
    type: str
"""

EXAMPLES = """
- name: Create a host in icinga
  t_systems_mms.icinga_director.icinga_host:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    disabled: false
    object_name: "foohost"
    address: "127.0.0.1"
    address6: "::1"
    display_name: "foohost"
    groups:
      - "foohostgroup"
    imports:
      - "foohosttemplate"
    vars:
      dnscheck: "no"
    check_command: hostalive
    notes: "example note"
    notes_url: "'http://url1' 'http://url2'"
    has_agent: true
    master_should_connect: true
    accept_config: true
    command_endpoint: fooendpoint
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
        disabled=dict(type="bool", default=False, choices=[True, False]),
        apply_to=dict(required=True, choices=["host", "service"]),
        assign_filter=dict(required=False),
        author=dict(required=True),
        comment=dict(required=True),
        duration=dict(required=False),
        fixed=dict(required=True, type="bool"),
        ranges=dict(type="dict", required=False, default={}),
        with_services=dict(default="y", choices=["y", "n"])

    )

    # When deleting objects, only the name is necessary, so we cannot use
    # required=True in the argument_spec. Instead we define here what is
    # necessary when state is present
    # required_if = [("state", "present", ["imports"])]

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    #   required_if=required_if,
    )

    data = {
        "object_name": module.params["object_name"],
        "object_type": "apply",
        "disabled": module.params["disabled"],
        "apply_to": module.params["apply_to"],
        "assign_filter": module.params["assign_filter"],
        "author": module.params["author"],
        "comment": module.params["comment"],
        "duration": module.params["duration"],
        "fixed": module.params["fixed"],
        "ranges": module.params["ranges"],
        "with_services": module.params["with_services"],
    }

    icinga_object = Icinga2APIObject(module=module, path="/scheduled-downtime", data=data)

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
