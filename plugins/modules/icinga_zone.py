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
module: icinga_zone
short_description: Manage zones in Icinga2
description:
   - Add or remove a zone to Icinga2 through the director API.
author: Aaron Bulmahn (@arbu)
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
version_added: '1.5.0'
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
      - Icinga object name for this zone.
      - This is usually a fully qualified host name but it could basically be any kind of string.
      - To make things easier for your users we strongly suggest to use meaningful names for templates.
      - For example "generic-zone" is ugly, "Standard Linux Server" is easier to understand.
    aliases: ['name']
    required: true
    type: str
  is_global:
    description:
      - Whether configuration files for this zone should be synced to all endpoints.
    default: false
    type: bool
  parent:
    description:
      - The name of the parent zone.
    type: str
"""

EXAMPLES = """
- name: Create a zone in icinga
  t_systems_mms.icinga_director.icinga_zone:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: "foozone"
    parent: "master"
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
        is_global=dict(required=False, type="bool", default=False),
        parent=dict(required=False),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    data = {
        "object_name": module.params["object_name"],
        "object_type": "object",
        "is_global": module.params["is_global"],
        "parent": module.params["parent"],
    }

    icinga_object = Icinga2APIObject(module=module, path="/zone", data=data)

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
