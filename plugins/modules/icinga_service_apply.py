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
module: icinga_service_apply
short_description: Manage service apply rules in Icinga2.
description:
   - "Add or remove a service apply rule to Icinga2 through the director API."
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
      - Name for the Icinga service apply rule.
    aliases: ['name']
    required: true
    type: str
  display_name:
    description:
      - Alternative displayed name of the service apply rule.
    required: false
    type: str
  check_command:
    description:
      - Check command definition.
    required: false
    type: str
    version_added: '1.7.0'
  groups:
    description:
      - Service groups that should be directly assigned to this service.
      - Servicegroups can be useful for various reasons.
      - They are helpful to provided service-type specific view in Icinga Web 2, either for custom dashboards or as an instrument to enforce restrictions.
      - Service groups can be directly assigned to single services or to service templates.
    required: false
    type: "list"
    elements: str
  apply_for:
    description:
      - Evaluates the apply for rule for all objects with the custom attribute specified.
      - E.g selecting "host.vars.custom_attr" will generate "for (config in host.vars.array_var)" where "config"
        will be accessible through "$config$". NOTE - only custom variables of type "Array" are eligible.
    required: false
    type: str
  assign_filter:
    description:
      - The filter where the service apply rule will take effect.
    required: false
    type: str
  imports:
    description:
      - Importable templates, add as many as you want.
      - Please note that order matters when importing properties from multiple templates - last one wins.
    required: false
    type: "list"
    elements: str
  vars:
    description:
      - Custom properties of the service apply rule.
    required: false
    type: "dict"
  notes:
    description:
      - Additional notes for this object.
    required: false
    type: str
  notes_url:
    description:
      - An URL pointing to additional notes for this object.
      - Separate multiple urls like this "'http://url1' 'http://url2'".
      - Maximum length is 255 characters.
    required: false
    type: str
"""

EXAMPLES = """
- name: Add service apply rule to icinga
  t_systems_mms.icinga_director.icinga_service_apply:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: "SERVICE_dummy"
    assign_filter: 'host.name="foohost"'
    check_command: hostalive
    display_name: "dummy process"
    imports:
      - fooservicetemplate
    groups:
      - fooservicegroup
    vars:
      http_address: "$address$"
      http_port: "9080"
      http_uri: "/ready"
      http_string: "Ready"
      http_expect: "Yes"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec
from ansible_collections.t_systems_mms.icinga_director.plugins.module_utils.icinga import (
    Icinga2APIObject,
)


# ===========================================
# Icinga2 API class
#
class ServiceApplyRule(Icinga2APIObject):
    def __init__(self, module, data):
        path = "/service"
        super(ServiceApplyRule, self).__init__(module, path, data)

    def exists(self):
        ret = self.call_url(path="/serviceapplyrules")
        if ret["code"] == 200:
            for existing_rule in ret["data"]["objects"]:
                if existing_rule["object_name"] == self.data["object_name"]:
                    self.object_id = existing_rule["id"]
                    return self.object_id
        return False

    def delete(self):
        return super(ServiceApplyRule, self).delete(find_by="id")

    def modify(self):
        return super(ServiceApplyRule, self).modify(find_by="id")

    def diff(self):
        return super(ServiceApplyRule, self).diff(find_by="id")


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
        object_name=dict(required=True, aliases=["name"]),
        display_name=dict(required=False),
        check_command=dict(required=False),
        apply_for=dict(required=False),
        assign_filter=dict(required=False),
        imports=dict(type="list", elements="str", required=False),
        groups=dict(type="list", elements="str", default=[], required=False),
        vars=dict(type="dict", default={}),
        notes=dict(type="str", required=False),
        notes_url=dict(type="str", required=False),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    data = {
        "object_name": module.params["object_name"],
        "display_name": module.params["display_name"],
        "object_type": "apply",
        "apply_for": module.params["apply_for"],
        "check_command": module.params["check_command"],
        "assign_filter": module.params["assign_filter"],
        "imports": module.params["imports"],
        "groups": module.params["groups"],
        "vars": module.params["vars"],
        "notes": module.params["notes"],
        "notes_url": module.params["notes_url"],
    }

    icinga_object = ServiceApplyRule(module=module, data=data)

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
