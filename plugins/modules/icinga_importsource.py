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
module: icinga_importsource
short_description: Manage import sources in Icinga2 Director
description:
   - Add or remove an import source in Icinga2 Director through the director API.
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
  source_name:
    description:
      - Name of the import source.
      - This must be unique across all import sources in Icinga Director.
    aliases: ['name']
    required: true
    type: str
  key_column:
    description:
      - The column name to use as the unique key for imported rows.
      - This column must be present in every imported row and must be unique.
      - Required when creating a new import source.
    required: false
    type: str
  provider_class:
    description:
      - The fully-qualified PHP class name of the import source provider.
      - Examples are C(Icinga\\Module\\Director\\Import\\RestApiImportSource),
        C(Icinga\\Module\\Director\\Import\\LdapImportSource) or
        C(Icinga\\Module\\Director\\Import\\DbImportSource).
      - Required when creating a new import source.
    required: false
    type: str
  description:
    description:
      - An optional description for this import source.
    required: false
    type: str
  settings:
    description:
      - A dict of provider-specific settings that are stored as key-value pairs
        in the Director import_source_setting table.
      - The available keys depend on the chosen C(provider_class).
      - "Example for the OTC provider: C(iam_url), C(username), C(password), C(domain), C(project), C(service_type), C(resource_path)."
    required: false
    type: dict
  modifiers:
    description:
      - A list of row modifier objects to apply to imported rows.
      - Each modifier is a dict with keys C(property_name), C(target_property),
        C(provider_class) and C(settings).
      - For a regex modifier that extracts an IP address, set C(provider_class) to
        C(Icinga\\Module\\Director\\PropertyModifier\\PropertyModifierRegexReplace).
    required: false
    type: list
    elements: dict
  append:
    description:
      - Do not overwrite the whole object but instead append the defined properties.
      - Note - Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.
      - Note - Variables that are set by default will also be applied, even if not set.
    type: bool
    choices: [true, false]
    version_added: '2.0.0'
"""

EXAMPLES = r"""
- name: Create an import source in icinga
  telekom_mms.icinga_director.icinga_importsource:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    source_name: "My Import Source"
    key_column: "hostname"
    provider_class: "Icinga\\Module\\Director\\Import\\RestApiImportSource"
    description: "Import hosts from REST API"

- name: Update the description of an import source
  telekom_mms.icinga_director.icinga_importsource:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    source_name: "My Import Source"
    description: "Updated description"
    append: true

- name: Delete an import source in icinga
  telekom_mms.icinga_director.icinga_importsource:
    state: absent
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    source_name: "My Import Source"
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
# Icinga2 API class for Import Sources.
#
class ImportSourceObject(Icinga2APIObject):
    """
    Icinga2 Director Import Source API object.

    Uses the standard /director/importsources (plural) bulk endpoint, which is
    available in unpatched Director installations (>= 1.3).  This avoids the
    need for the icingaweb2-module-otc ImportsourceController patch for
    create / modify / read operations.

    Note: state=absent (delete) still falls back to the singular
    /director/importsource?name=X endpoint, which requires the patched
    controller on the Director server.
    """

    # Fields compared when deciding whether a modify POST is needed.
    _BULK_KEYS = frozenset(
        ["source_name", "provider_class", "key_column", "description", "settings", "modifiers"]
    )

    def __init__(self, module, path, data):
        super().__init__(module, path, data)
        self._current = None  # populated by exists()

    def _desired_payload(self):
        """
        Build a single import-source object in the ImportExport bulk format
        expected by POST /director/importsources.

        In append mode unset core fields fall back to the current Director
        value; settings are merged (new keys win).
        """
        current = self._current or {}
        append = self.data.get("_append", False)

        settings = self.data.get("settings") or {}
        if append:
            merged = dict(current.get("settings") or {})
            merged.update(settings)
            settings = merged

        def _val(key):
            v = self.data.get(key)
            if v is None and append:
                return current.get(key)
            return v

        desired_modifiers = self.data.get("modifiers")
        if desired_modifiers is None:
            # not specified in task → preserve whatever is already in Director
            modifiers = current.get("modifiers", [])
        else:
            modifiers = desired_modifiers

        return {
            "source_name": self.data["source_name"],
            "provider_class": _val("provider_class"),
            "key_column": _val("key_column"),
            "description": _val("description"),
            "modifiers": modifiers,
            "settings": settings,
        }

    @staticmethod
    def _norm_modifiers(modifiers):
        """Strip read-only fields (priority) from modifier list for comparison."""
        _skip = {"priority", "description", "filter_expression"}
        result = []
        for m in (modifiers or []):
            result.append({k: v for k, v in m.items() if k not in _skip})
        return result

    def exists(self):
        """GET /director/importsources and search the list by source_name."""
        ret = self.call_url(path=self.path)
        if ret["code"] != 200:
            self.module.fail_json(
                msg="bad return code while querying: %d. Error message: %s"
                % (ret["code"], ret["error"])
            )
        sources = ret["data"] if isinstance(ret["data"], list) else []
        name = self.data["source_name"]
        for source in sources:
            if source.get("source_name") == name:
                self._current = source
                self.object_id = to_text(urlquote(name))
                return True
        self._current = None
        return False

    def create(self):
        """POST a single-element array to /director/importsources."""
        ret = self.call_url(
            path=self.path,
            data=self.module.jsonify([self._desired_payload()]),
            method="POST",
        )
        # Bulk endpoint returns HTTP 200 + empty body on success.
        # Translate to 201 so base update() treats it as "created".
        if ret["code"] == 200:
            ret["code"] = 201
        return ret

    def modify(self):
        """
        Compare desired state with current state from Director.
        POST only when something actually changed; return synthetic 304 if not.
        """
        desired = self._desired_payload()
        current = self._current or {}

        # Compare all bulk keys except modifiers (needs normalization)
        scalar_keys = self._BULK_KEYS - {"modifiers"}
        scalar_equal = all(current.get(k) == desired.get(k) for k in scalar_keys)
        mods_equal = (
            self._norm_modifiers(current.get("modifiers", []))
            == self._norm_modifiers(desired.get("modifiers", []))
        )
        if scalar_equal and mods_equal:
            return {"code": 304, "data": {}, "error": ""}
        ret = self.call_url(
            path=self.path,
            data=self.module.jsonify([desired]),
            method="POST",
        )
        return ret

    def diff(self, find_by="name"):
        """Build a diff dict from stored _current vs _desired_payload."""
        current = self._current or {}
        desired = self._desired_payload()
        before = {}
        after = {}
        for key in self._BULK_KEYS:
            cv = current.get(key)
            dv = desired.get(key)
            if cv != dv:
                before[key] = cv
                after[key] = dv
        return {"before": before, "after": after} if before else {}

    def delete(self, find_by="name"):
        """
        DELETE via the singular /director/importsource?name=X endpoint.
        Requires the icingaweb2-module-otc ImportsourceController patch on the
        Director server.
        """
        return self.call_url(
            path="/importsource?name=" + self.object_id,
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
        source_name=dict(required=True, aliases=["name"]),
        key_column=dict(required=False, no_log=False),
        provider_class=dict(required=False),
        description=dict(required=False),
        settings=dict(required=False, type="dict", no_log=False),
        modifiers=dict(required=False, type="list", elements="dict"),
        api_timeout=dict(required=False, default=10, type="int"),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    data_keys = [
        "source_name",
        "key_column",
        "provider_class",
        "description",
    ]

    data = {}

    if module.params["append"]:
        for k in data_keys:
            if module.params[k]:
                data[k] = module.params[k]
    else:
        for k in data_keys:
            data[k] = module.params[k]

    if module.params["settings"]:
        data["settings"] = module.params["settings"]
    else:
        data["settings"] = {}

    if module.params.get("modifiers") is not None:
        data["modifiers"] = module.params["modifiers"]

    # Pass the append flag through data so _desired_payload() can use it.
    data["_append"] = bool(module.params.get("append"))

    # Set object_name as alias for source_name to satisfy base class update()
    # during check mode. The create() and modify() overrides strip this key
    # before sending to the API.
    data["object_name"] = data["source_name"]

    icinga_object = ImportSourceObject(
        module=module, path="/importsources", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
