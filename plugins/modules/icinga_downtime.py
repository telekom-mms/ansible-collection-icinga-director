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
module: icinga_downtime
short_description: Manage downtimes in Icinga2
description:
   - Add or remove a downtime to Icinga2 through the director API.
author: Daniel Uhlmann (@xFuture603)
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
version_added: '1.24.0'
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
  disabled:
    description:
      - Disabled objects will not be deployed.
    default: False
    type: bool
    choices: [True, False]
"""

EXAMPLES = """
  - name: create icinga_downtime
    t_systems_mms.icinga_director.icinga_downtime:
      url: "{{ icinga_url }}"
      url_username: "{{ icinga_user }}"
      url_password: "{{ icinga_pass }}"
      disabled: False
      object_name: "foodowntime"
      state: present
      author: testuser
      comment: test
      fixed: True
      with_services: True
      apply_to: host
      assign_filter: 'host.name="foohost"'
      duration: 500
      ranges:
        "tuesday": "00:00-24:00"
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
        url=dict(required=True), #not need in documentation
        object_name=dict(required=True, aliases=["name"]),
        disabled=dict(type="bool", default=False, choices=[True, False]),
        apply_to=dict(required=True, choices=["host", "service"]),
        assign_filter=dict(required=False),
        author=dict(required=True),
        comment=dict(required=True),
        duration=dict(required=False),
        fixed=dict(required=True, type="bool"),
        ranges=dict(type="dict", required=False, default={}),
        with_services=dict(type="bool", default=True, choices=[True, False])

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

    # Icinga expects 'y' or 'n' instead of booleans
    if module.params["with_services"]:
      _withservices = "y"
    else:
      _withservices = "n"

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
        "with_services": _withservices,
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
