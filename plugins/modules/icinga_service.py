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
module: icinga_service
short_description: Manage services in Icinga2
description:
   - Add or remove a service to Icinga2 through the director API.
author: Sebastian Gumprich (@rndmh3ro)
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
version_added: '1.0.0'
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
      - Name of the service.
    aliases: ['name']
    required: true
    type: str
  check_command:
    description:
      - Check command definition.
    type: str
  check_interval:
    description:
      - Your regular check interval.
    type: str
  check_period:
    description:
      - The name of a time period which determines when this object should be monitored. Not limited by default.
    type: str
  check_timeout:
    description:
      - Check command timeout in seconds. Overrides the CheckCommand's timeout attribute.
    type: str
  enable_active_checks:
    description:
      - Whether to actively check this object.
    type: "bool"
  enable_event_handler:
    description:
      - Whether to enable event handlers this object.
    type: "bool"
  enable_notifications:
    description:
      - Whether to send notifications for this object.
    type: "bool"
  enable_passive_checks:
    description:
      - Whether to accept passive check results for this object.
    type: "bool"
  enable_perfdata:
    description:
      - Whether to process performance data provided by this object.
    type: "bool"
  groups:
    description:
      - Service groups that should be directly assigned to this service.
      - Servicegroups can be useful for various reasons.
      - They are helpful to provided service-type specific view in Icinga Web 2, either for custom dashboards or as an instrument to enforce restrictions.
      - Service groups can be directly assigned to single services or to service templates.
    type: "list"
    elements: "str"
    default: []
  host:
    description:
      - Choose the host this single service should be assigned to.
    required: true
    type: "str"
  imports:
    description:
      - Importable templates, add as many as you want.
      - Please note that order matters when importing properties from multiple templates - last one wins.
    type: "list"
    elements: "str"
    default: []
  max_check_attempts:
    description:
      - Defines after how many check attempts a new hard state is reached.
    type: str
  notes:
    description:
      - Additional notes for this object.
    type: str
    version_added: '1.8.0'
  notes_url:
    description:
      - An URL pointing to additional notes for this object.
      - Separate multiple urls like this "'http://url1' 'http://url2'".
      - Maximum length is 255 characters.
    type: str
    version_added: '1.8.0'
  retry_interval:
    description:
      - Retry interval, will be applied after a state change unless the next hard state is reached.
    type: str
  use_agent:
    description:
      - Whether the check command for this service should be executed on the Icinga agent.
    type: "bool"
  vars:
    description:
      - Custom properties of the service.
    type: "dict"
    default: {}
  volatile:
    description:
      - Whether this check is volatile.
    type: "bool"
  disabled:
    description:
      - Disabled objects will not be deployed.
    type: bool
    default: False
    choices: [True, False]
  append:
    description:
      - Do not overwrite the whole object but instead append the defined properties.
      - Note - Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.
    type: bool
    choices: [True, False]
    version_added: '1.25.0'
"""

EXAMPLES = """
- name: Create service
  tags: service
  t_systems_mms.icinga_director.icinga_service:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: "foo service"
    check_command: hostalive
    use_agent: false
    host: foohost
    vars:
      procs_argument: consul
      procs_critical: '1:'
      procs_warning: '1:'

- name: Update service
  tags: service
  t_systems_mms.icinga_director.icinga_service:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: "foo service"
    host: foohost
    notes: "example note"
    notes_url: "'http://url1' 'http://url2'"
    append: true
"""

RETURN = r""" # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec
from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.six.moves.urllib.parse import quote as urlquote
from ansible_collections.t_systems_mms.icinga_director.plugins.module_utils.icinga import (
    Icinga2APIObject,
)
import json
from collections import defaultdict


class IcingaServiceObject(Icinga2APIObject):
    module = None

    def __init__(self, module, path, data):
        super(IcingaServiceObject, self).__init__(module, path, data)
        self.module = module
        self.params = module.params
        self.path = path
        self.data = data
        self.object_id = None

    def exists(self, find_by="name"):
        ret = super(IcingaServiceObject, self).call_url(
            path="/service"
            + "?"
            + "name="
            + to_text(urlquote(self.data["object_name"]))
            + "&"
            + "host="
            + to_text(urlquote(self.data["host"]))
        )
        self.object_id = to_text(urlquote(self.data["object_name"]))
        if ret["code"] == 200:
            return True
        return False

    def delete(self, find_by="name"):
        ret = super(IcingaServiceObject, self).call_url(
            path="/service"
            + "?"
            + "name="
            + to_text(urlquote(self.data["object_name"]))
            + "&"
            + "host="
            + to_text(urlquote(self.data["host"])),
            method="DELETE",
        )
        return ret

    def modify(self, find_by="name"):
        ret = super(IcingaServiceObject, self).call_url(
            path="/service"
            + "?"
            + "name="
            + to_text(urlquote(self.data["object_name"]))
            + "&"
            + "host="
            + to_text(urlquote(self.data["host"])),
            data=self.module.jsonify(self.data),
            method="POST",
        )
        return ret

    def diff(self, find_by="name"):
        ret = super(IcingaServiceObject, self).call_url(
            path="/service"
            + "?"
            + "name="
            + to_text(urlquote(self.data["object_name"]))
            + "&"
            + "host="
            + to_text(urlquote(self.data["host"])),
            method="GET",
        )

        data_from_director = json.loads(self.module.jsonify(ret["data"]))
        data_from_task = json.loads(self.module.jsonify(self.data))

        diff = defaultdict(dict)
        for key, value in data_from_director.items():
            value = self.scrub_diff_value(value)
            if key in data_from_task.keys() and value != data_from_task[key]:
                diff["before"][key] = "{val}".format(val=value)
                diff["after"][key] = "{val}".format(val=data_from_task[key])

        return diff


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
        disabled=dict(type="bool", default=False, choices=[True, False]),
        check_command=dict(required=False),
        check_interval=dict(required=False),
        check_period=dict(required=False),
        check_timeout=dict(required=False),
        enable_active_checks=dict(type="bool", required=False),
        enable_event_handler=dict(type="bool", required=False),
        enable_notifications=dict(type="bool", required=False),
        enable_passive_checks=dict(type="bool", required=False),
        enable_perfdata=dict(type="bool", required=False),
        host=dict(required=True),
        groups=dict(type="list", elements="str", default=[], required=False),
        imports=dict(type="list", elements="str", default=[], required=False),
        max_check_attempts=dict(required=False),
        notes=dict(type="str", required=False),
        notes_url=dict(type="str", required=False),
        retry_interval=dict(required=False),
        use_agent=dict(type="bool", required=False),
        vars=dict(type="dict", default={}, required=False),
        volatile=dict(type="bool", required=False),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    data = {
        "object_name": module.params["object_name"],
        "disabled": module.params["disabled"],
        "check_command": module.params["check_command"],
        "check_interval": module.params["check_interval"],
        "check_period": module.params["check_period"],
        "check_timeout": module.params["check_timeout"],
        "enable_active_checks": module.params["enable_active_checks"],
        "enable_event_handler": module.params["enable_event_handler"],
        "enable_notifications": module.params["enable_notifications"],
        "enable_passive_checks": module.params["enable_passive_checks"],
        "enable_perfdata": module.params["enable_perfdata"],
        "groups": module.params["groups"],
        "host": module.params["host"],
        "imports": module.params["imports"],
        "max_check_attempts": module.params["max_check_attempts"],
        "notes": module.params["notes"],
        "notes_url": module.params["notes_url"],
        "retry_interval": module.params["retry_interval"],
        "use_agent": module.params["use_agent"],
        "vars": module.params["vars"],
        "volatile": module.params["volatile"],
    }

    if module.params["append"]:
        new_dict = {}
        for k in data:
            if module.params[k]:
                new_dict[k] = module.params[k]
        data = new_dict

    data["object_type"] = "object"

    icinga_object = IcingaServiceObject(
        module=module, path="/service", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
