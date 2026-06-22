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
  - Uses the standard C(/director/syncrules) bulk endpoint (GET/POST/DELETE).
    Requires Director with upstream PR adding POST and DELETE support to
    C(SyncrulesController) and C(unserializeSyncRules) in C(ImportExport).
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

    Uses the standard /director/syncrules (plural) bulk endpoint, available
    in Director >= 1.3 once the upstream PR adding POST/DELETE support has been
    merged.  This avoids any patched singular controller.

    Behaviour mirrors icinga_importsource:
      exists()  – GET /director/syncrules, search list by rule_name
      create()  – POST single-element array to /director/syncrules
      modify()  – same POST (unserialize is idempotent / upsert)
      delete()  – DELETE /director/syncrules?name=<name>
    """

    _BULK_KEYS = frozenset([
        "rule_name", "object_type", "update_policy",
        "purge_existing", "purge_action", "filter_expression", "description",
    ])

    def __init__(self, module, path, data):
        super().__init__(module, path, data)
        self._current = None  # populated by exists()

    def _desired_payload(self):
        """Build a single sync-rule object in the Director bulk export format."""
        current = self._current or {}
        append = self.data.get("_append", False)

        def _val(key):
            v = self.data.get(key)
            if v is None and append:
                return current.get(key)
            return v

        # Director stores purge_existing as "y"/"n"; NOT NULL in DB → default "n"
        purge = _val("purge_existing")
        if isinstance(purge, bool):
            purge = "y" if purge else "n"
        if purge is None:
            purge = "n"

        return {
            "rule_name": self.data["rule_name"],
            "object_type": _val("object_type"),
            "update_policy": _val("update_policy"),
            "purge_existing": purge,
            "purge_action": _val("purge_action"),
            "filter_expression": _val("filter_expression"),
            "description": _val("description"),
            # sync_properties are a related object – not a direct SyncRule property
            # and are not managed by this module
        }

    def exists(self):
        """GET /director/syncrules and search the list by rule_name."""
        ret = self.call_url(path=self.path)
        if ret["code"] != 200:
            self._current = None
            return False
        rules = ret["data"] if isinstance(ret["data"], list) else []
        name = self.data["rule_name"]
        for rule in rules:
            if rule.get("rule_name") == name:
                self._current = rule
                self.object_id = to_text(urlquote(name))
                return True
        self._current = None
        return False

    def create(self):
        """POST single-element array to /director/syncrules."""
        ret = self.call_url(
            path=self.path,
            data=self.module.jsonify([self._desired_payload()]),
            method="POST",
        )
        # Bulk endpoint returns HTTP 200 on success; translate to 201 so that
        # the base update() method treats the result as "created".
        if ret["code"] == 200:
            ret["code"] = 201
        return ret

    @staticmethod
    def _norm(val):
        """Normalize Director boolean variants (True/"y" and False/"n"/None) for comparison."""
        if val is True or val == "y":
            return "y"
        if val is False or val == "n" or val is None:
            return "n"
        return val

    def modify(self):
        """POST only when the desired state differs from the current state."""
        desired = self._desired_payload()
        current = self._current or {}
        if all(self._norm(current.get(k)) == self._norm(desired.get(k)) for k in self._BULK_KEYS):
            return {"code": 304, "data": {}, "error": ""}
        return self.call_url(
            path=self.path,
            data=self.module.jsonify([desired]),
            method="POST",
        )

    def diff(self, find_by="name"):
        """Return a before/after diff dict for changed _BULK_KEYS only."""
        current = self._current or {}
        desired = self._desired_payload()
        before, after = {}, {}
        for key in self._BULK_KEYS:
            cv, dv = current.get(key), desired.get(key)
            if self._norm(cv) != self._norm(dv):
                before[key] = cv
                after[key] = dv
        return {"before": before, "after": after} if before else {}

    def delete(self, find_by="name"):
        """DELETE /director/syncrules?name=<name>."""
        return self.call_url(
            path=self.path + "?name=" + self.object_id,
            method="DELETE",
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
        data["_append"] = True
        for k in data_keys:
            if module.params[k] is not None:
                data[k] = module.params[k]
    else:
        for k in data_keys:
            data[k] = module.params[k]

    # object_name is required by the base class update() / check-mode path
    data["object_name"] = data["rule_name"]

    icinga_object = SyncRuleObject(
        module=module, path="/syncrules", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
