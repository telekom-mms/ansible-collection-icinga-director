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

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: icinga_servicegroup
short_description: Manage servicegroup in Icinga2
description:
   - "Add or remove a servicegroup to Icinga2 through the director API."
author: Sebastian Gumprich (@rndmh3ro)
extends_documentation_fragment: t_systems_mms.icinga_director.auth_options
version_added: '1.0.0'
options:
  state:
    description:
      - Apply feature state.
    choices: [ "present", "absent" ]
    default: present
    type: str
  object_name:
    description:
      - Icinga object name for this servicegroup.
    required: true
    type: str
  display_name:
    description:
      - An alternative display name for this group.
        If you wonder how this could be helpful just leave it blank
    required: false
    type: str
  assign_filter:
    description:
      - This allows you to configure an assignment filter.
         Please feel free to combine as many nested operators as you want
    required: false
    type: str
"""

EXAMPLES = """
- name: create servicegroup
  t_systems_mms.icinga_director.icinga_servicegroup:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: fooservicegroup
    display_name: fooservicegroup
    assign_filter: 'host.name="foo"'
"""

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
    # remove unnecessary argument 'force'
    del argument_spec["force"]
    del argument_spec["http_agent"]
    # add our own arguments
    argument_spec.update(
        state=dict(default="present", choices=["absent", "present"]),
        url=dict(required=True),
        object_name=dict(required=True),
        display_name=dict(required=False),
        assign_filter=dict(required=False),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    data = {
        "object_name": module.params["object_name"],
        "object_type": "object",
        "display_name": module.params["display_name"],
        "assign_filter": module.params["assign_filter"],
    }

    icinga_object = Icinga2APIObject(
        module=module, path="/servicegroup", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        object_name=module.params["object_name"],
        data=icinga_object.data,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
