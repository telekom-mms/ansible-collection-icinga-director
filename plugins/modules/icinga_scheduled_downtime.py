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
module: icinga_scheduled_downtime
short_description: Manage downtimes in Icinga2
description:
   - Add or remove a downtime to Icinga2 through the director API.
author: Daniel Uhlmann (@xFuture603)
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
version_added: '1.25.0'
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
      - Icinga object name for this downtime.
    aliases: ['name']
    required: true
    type: str
  disabled:
    description:
      - Disabled objects will not be deployed.
    default: False
    type: bool
    choices: [True, False]
  author:
    description:
      - Name of the downtime author.
    required: true
    type: str
  comment:
    description:
      - A descriptive comment for the downtime.
    required: true
    type: str
  fixed:
    description:
      - Whether this downtime is fixed or flexible.
        If unsure please check the related documentation https://icinga.com/docs/icinga2/latest/doc/08-advanced-topics/#downtimes
    required: true
    type: bool
    choices: [True, False]
  with_services:
    description:
      - Whether you only downtime the hosts or add some services with it.
    type: bool
    choices: [True, False]
    default: True
  ranges:
    description:
      - The period which should be downtimed
    type: dict
  apply_to:
    description:
      - Whether this dependency should affect hosts or services
    type: str
    required: true
    choices: ["host", "service"]
  assign_filter:
    description:
      - The filter where the downtime will take effect.
    type: str
  duration:
    description:
      - How long the downtime lasts.
        Only has an effect for flexible (non-fixed) downtimes.
        Time in seconds, supported suffixes include ms (milliseconds), s (seconds), m (minutes), h (hours) and d (days).
        To express "90 minutes" you might want to write 1h 30m
    type: str
  append:
    description:
      - Do not overwrite the whole object but instead append the defined properties.
      - Note: Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.
    type: bool
    choices: [True, False]
    version_added: '1.25.0'
"""

EXAMPLES = """
- name: create icinga_scheduled_downtime
  t_systems_mms.icinga_director.icinga_scheduled_downtime:
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    disabled: false
    object_name: "foodowntime"
    state: present
    author: testuser
    comment: test
    fixed: true
    with_services: true
    apply_to: host
    assign_filter: 'host.name="foohost"'
    duration: 500
    ranges:
      "tuesday": "00:00-24:00"

- name: create icinga_scheduled_downtime2
  t_systems_mms.icinga_director.icinga_scheduled_downtime:
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    disabled: false
    object_name: "foodowntime2"
    state: present
    author: testuser
    comment: test
    fixed: false
    with_services: false
    apply_to: host
    assign_filter: 'host.name="foohost"'
    duration: 500
    ranges:
      "tuesday": "00:00-24:00"

- name: update icinga_scheduled_downtime2
  t_systems_mms.icinga_director.icinga_scheduled_downtime:
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: "foodowntime2"
    state: present
    duration: 1000
    append: true
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
        append=dict(type="bool", choices=[True, False]),
        object_name=dict(required=True, aliases=["name"]),
        disabled=dict(type="bool", default=False, choices=[True, False]),
        apply_to=dict(choices=["host", "service"]),
        assign_filter=dict(required=False),
        author=dict(),
        comment=dict(),
        duration=dict(required=False),
        fixed=dict(type="bool", choices=[True, False]),
        ranges=dict(type="dict", required=False, default={}),
        with_services=dict(type="bool", default=True, choices=[True, False]),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    # When deleting objects, only the name is necessary, so we cannot use
    # required=True in the argument_spec. Instead we define here what is
    # necessary when state is present and we do not append to an existing object
    if module.params["append"]:
        module.required_if = ""
    else:
        module.required_if = [
            ("state", "present", ["apply_to", "author", "comment", "fixed"])
        ]

    # Icinga expects 'y' or 'n' instead of booleans for option "with_services"
    if module.params["with_services"]:
        _withservices = "y"
    else:
        _withservices = "n"

    # Icinga expects 'yes' or 'no' instead of booleans for option "fixed"
    if module.params["fixed"]:
        _fixed = "y"
    else:
        _fixed = "n"

    data = {
        "object_name": module.params["object_name"],
        "disabled": module.params["disabled"],
        "apply_to": module.params["apply_to"],
        "assign_filter": module.params["assign_filter"],
        "author": module.params["author"],
        "comment": module.params["comment"],
        "duration": module.params["duration"],
        "fixed": _fixed,
        "ranges": module.params["ranges"],
        "with_services": _withservices,
    }

    if module.params["append"]:
        new_dict = {}
        for k in data:
            if module.params[k]:
                new_dict[k] = module.params[k]
        data = new_dict

    data["object_type"] = "apply"

    icinga_object = Icinga2APIObject(
        module=module, path="/scheduled-downtime", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
