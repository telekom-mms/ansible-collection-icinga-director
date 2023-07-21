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
module: icinga_timeperiod
short_description: Manage timeperiods in Icinga2
description:
   - Add or remove a timeperiod to Icinga2 through the director API.
author: Sebastian Gumprich (@rndmh3ro)
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
version_added: '1.0.0'
notes:
  - This module supports check mode.
deprecated:
  why: moved collection to new organisation telekom_mms
  removed_in: 3.0.0
  alternative: telekom_mms.icinga_director.icinga_timeperiod
options:
  state:
    description:
      - Apply feature state.
    choices: [ "present", "absent" ]
    default: present
    type: str
  object_name:
    description:
      - Name of the time period.
    aliases: ['name']
    required: true
    type: str
  display_name:
    description:
      - Alternative name for this timeperiod.
    type: str
  imports:
    description:
      - Importable templates, add as many as you want.
      - Please note that order matters when importing properties from multiple templates - last one wins.
    type: list
    elements: str
    default: []
  ranges:
    description:
      - A dict of days and timeperiods.
    type: dict
  append:
    description:
      - Do not overwrite the whole object but instead append the defined properties.
      - Note - Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.
      - Note - Variables that are set by default will also be applied, even if not set.
    type: bool
    choices: [true, false]
    version_added: '1.25.0'
"""

EXAMPLES = """
- name: Create timeperiod
  t_systems_mms.icinga_director.icinga_timeperiod:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: '24/7'
    imports:
      - "timeperiod_template"
    ranges:
      monday: "00:00-23:59"
      tuesday: "00:00-23:59"
      wednesday: "00:00-23:59"
      thursday: "00:00-23:59"
      friday: "00:00-23:59"
      saturday: "00:00-23:59"
      sunday: "00:00-23:59"

- name: Update timeperiod
  t_systems_mms.icinga_director.icinga_timeperiod:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: '24/7'
    display_name: '24/7'
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
        display_name=dict(required=False),
        imports=dict(type="list", elements="str", default=[], required=False),
        ranges=dict(type="dict", required=False),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    data_keys = [
        "object_name",
        "display_name",
        "imports",
        "ranges",
    ]

    data = {}

    if module.params["append"]:
        for k in data_keys:
            if module.params[k]:
                data[k] = module.params[k]
    else:
        for k in data_keys:
            data[k] = module.params[k]

    data["object_type"] = "object"

    icinga_object = Icinga2APIObject(
        module=module, path="/timeperiod", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
