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

    Import sources are not standard Icinga objects and use 'source_name' as
    their identifier instead of 'object_name'. This subclass adapts the base
    class to use the correct field names and API endpoints.
    """

    def exists(self):
        ret = self.call_url(
            path=self.path
            + "?name="
            + to_text(urlquote(self.data["source_name"]))
        )
        self.object_id = to_text(urlquote(self.data["source_name"]))
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
        source_name=dict(required=True, aliases=["name"]),
        key_column=dict(required=False),
        provider_class=dict(required=False),
        description=dict(required=False),
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

    # Set object_name as alias for source_name to satisfy base class update()
    # during check mode. The create() and modify() overrides strip this key
    # before sending to the API.
    data["object_name"] = data["source_name"]

    icinga_object = ImportSourceObject(
        module=module, path="/importsource", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
