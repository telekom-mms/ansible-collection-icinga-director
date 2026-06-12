#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 T-Systems Multimedia Solutions GmbH
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
module: icinga_syncrule
short_description: Manage sync rules in Icinga2 Director
description:
   - Add or remove a sync rule in Icinga2 Director through the director API.
author: Michaela Mattes (@mikaEz)
extends_documentation_fragment:
  - ansible.builtin.url
  - telekom_mms.icinga_director.common_options
version_added: '2.0.0'
notes:
  - This module supports check mode.
options:
  state:
    description:
      - Apply feature state.
    choices: [ "present", "absent" ]
    default: present
    type: str
  rule_name:
    description:
      - Name of the sync rule.
      - This must be unique across all sync rules in Icinga Director.
    aliases: ['name']
    required: true
    type: str
  object_type:
    description:
      - The Icinga object type that this sync rule targets.
      - This is the type of Icinga object that will be created or updated by the sync rule,
        not to be confused with the Director object_type (object/template/apply).
    choices:
      - host
      - service
      - command
      - user
      - hostgroup
      - servicegroup
      - usergroup
      - datalistEntry
      - endpoint
      - zone
      - timePeriod
      - serviceSet
      - scheduledDowntime
      - notification
      - dependency
    required: false
    type: str
  update_policy:
    description:
      - Defines how existing Icinga objects are updated when the sync rule runs.
      - C(merge) merges properties from the import source with existing object properties.
      - C(override) replaces all properties of existing objects with values from the import source.
      - C(ignore) does not modify existing objects, only creates new ones.
      - C(update-only) only updates existing objects, never creates new ones.
    choices: [ "merge", "override", "ignore", "update-only" ]
    required: false
    type: str
  purge_existing:
    description:
      - Whether to remove Icinga objects that are no longer present in the import source.
    required: false
    type: bool
  purge_action:
    description:
      - Action to take when purging objects that no longer exist in the import source.
      - Only relevant when C(purge_existing) is C(true).
    choices: [ "delete", "disable" ]
    required: false
    type: str
  filter_expression:
    description:
      - An optional filter expression to restrict which imported rows are processed by this sync rule.
    required: false
    type: str
  description:
    description:
      - An optional description for this sync rule.
    required: false
    type: str
  append:
    description:
      - Do not overwrite the whole object but instead append the defined properties.
      - Note - Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.
      - Note - Variables that are set by default will also be applied, even if not set.
    type: bool
    choices: [true, false]
    version_added: '2.0.0'
"""

EXAMPLES = """
- name: Create a sync rule in icinga
  telekom_mms.icinga_director.icinga_syncrule:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    rule_name: "Sync Hosts from CMDB"
    object_type: "host"
    update_policy: "merge"
    purge_existing: false
    description: "Synchronizes hosts from the CMDB import source"

- name: Create a sync rule that purges deleted objects
  telekom_mms.icinga_director.icinga_syncrule:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    rule_name: "Sync Services from CMDB"
    object_type: "service"
    update_policy: "override"
    purge_existing: true
    purge_action: "disable"
    filter_expression: 'source.vars.monitored="yes"'

- name: Update the description of a sync rule
  telekom_mms.icinga_director.icinga_syncrule:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    rule_name: "Sync Hosts from CMDB"
    description: "Updated description"
    append: true

- name: Delete a sync rule in icinga
  telekom_mms.icinga_director.icinga_syncrule:
    state: absent
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    rule_name: "Sync Hosts from CMDB"
"""

RETURN = r""" # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec
from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.six.moves.urllib.parse import quote as urlquote
from ansible_collections.telekom_mms.icinga_director.plugins.module_utils.icinga import (
    Icinga2APIObject,
)


# ===========================================
# Icinga2 API class for Sync Rules.
#
class SyncRuleObject(Icinga2APIObject):
    """
    Icinga2 Director Sync Rule API object.

    Sync rules are not standard Icinga objects and use 'rule_name' as their
    identifier instead of 'object_name'. This subclass adapts the base class
    to use the correct field names and API endpoints.
    """

    def exists(self):
        ret = self.call_url(
            path=self.path
            + "?name="
            + to_text(urlquote(self.data["rule_name"]))
        )
        self.object_id = to_text(urlquote(self.data["rule_name"]))
        return ret["code"] == 200

    def create(self):
        api_data = {k: v for k, v in self.data.items() if k != "object_name"}
        return self.call_url(
            path=self.path,
            data=self.module.jsonify(api_data),
            method="POST",
        )

    def modify(self):
        api_data = {k: v for k, v in self.data.items() if k != "object_name"}
        return self.call_url(
            path=self.path + "?name=" + self.object_id,
            data=self.module.jsonify(api_data),
            method="POST",
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
        rule_name=dict(required=True, aliases=["name"]),
        object_type=dict(
            required=False,
            choices=[
                "host",
                "service",
                "command",
                "user",
                "hostgroup",
                "servicegroup",
                "usergroup",
                "datalistEntry",
                "endpoint",
                "zone",
                "timePeriod",
                "serviceSet",
                "scheduledDowntime",
                "notification",
                "dependency",
            ],
        ),
        update_policy=dict(
            required=False,
            choices=["merge", "override", "ignore", "update-only"],
        ),
        purge_existing=dict(type="bool", required=False),
        purge_action=dict(
            required=False, choices=["delete", "disable"]
        ),
        filter_expression=dict(required=False),
        description=dict(required=False),
        api_timeout=dict(required=False, default=10, type="int"),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    data_keys = [
        "rule_name",
        "object_type",
        "update_policy",
        "purge_existing",
        "purge_action",
        "filter_expression",
        "description",
    ]

    data = {}

    if module.params["append"]:
        for k in data_keys:
            if module.params[k] is not None:
                data[k] = module.params[k]
    else:
        for k in data_keys:
            data[k] = module.params[k]

    # Set object_name as alias for rule_name to satisfy base class update()
    # during check mode. The create() and modify() overrides strip this key
    # before sending to the API.
    data["object_name"] = data["rule_name"]

    icinga_object = SyncRuleObject(
        module=module, path="/syncrule", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
