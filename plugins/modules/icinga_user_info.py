#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 T-Systems Multimedia Solutions GmbH
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
module: icinga_user_info
short_description: Query users in Icinga2
description:
   - Get a list of user objects from Icinga2 through the director API.
author: Martin Schurz (@schurzi)
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
version_added: '1.13.0'
notes:
  - This module supports check mode.
options:
  query:
    description:
      - Text to filter search results.
      - The text is matched on object_name.
      - Only objects containing this text will be returned in the resultset.
      - Requires Icinga Director 1.8.0+, in earlier versions this parameter is ignored and all objects are returned.
    required: false
    type: str
    default: ""
  resolved:
    description:
      - Resolve all inherited object properties and omit templates in output.
    type: bool
    default: False
    choices: [True, False]
"""

EXAMPLES = """
- name: Query a user in icinga
  t_systems_mms.icinga_director.icinga_user_info:
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    query: "rb"
"""

RETURN = r"""
objects:
  description:
    - A list of returned Director objects.
    - The list contains all objects matching the query filter.
    - If the filter does not match any object, the list will be empty.
  returned: always
  type: list
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
    # add our own arguments
    argument_spec.update(
        url=dict(required=True),
        query=dict(type="str", required=False, default=""),
        resolved=dict(type="bool", default=False, choices=[True, False]),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    icinga_object = Icinga2APIObject(module=module, path="/users", data=[])

    object_list = icinga_object.query(
        query=module.params["query"], resolved=module.params["resolved"]
    )
    module.exit_json(
        objects=object_list["data"]["objects"],
    )


# import module snippets
if __name__ == "__main__":
    main()
