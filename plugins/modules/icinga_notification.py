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
module: icinga_notification
short_description: Manage notifications in Icinga2
description:
   - "Add or remove a notification to Icinga2 through the director API."
author: Sebastian Gumprich (@rndmh3ro)
extends_documentation_fragment: t_systems_mms.icinga_director.auth_options
options:
  state:
    description:
      - Apply feature state.
    choices: [ "present", "absent" ]
    default: present
    type: str
  object_name:
    description:
      - Name of the notification
    required: true
    type: str
  notification_interval:
    description:
      - The notification interval (in seconds). This interval is used for active notifications.
      - Defaults to 30 minutes. If set to 0, re-notifications are disabled.
    required: false
    type: str
  types:
    description:
      - The state transition types you want to get notifications for
    required: false
    type: "list"
    elements: str
  users:
    description:
      - Users that should be notified by this notifications
    required: false
    type: "list"
    elements: str
  states:
    description:
      - The host/service states you want to get notifications for
    required: false
    type: "list"
    elements: str
  apply_to:
    description:
      - Whether this notification should affect hosts or services
    required: true
    type: str
    choices: ["host", "service"]
  assign_filter:
    description:
      - The filter where the service apply rule will take effect
    required: false
    type: "str"
  imports:
    description:
      - Importable templates, add as many as you want. Required when state is C(present).
        Please note that order matters when importing properties from multiple templates - last one wins
    type: "list"
    elements: str
  disabled:
    description:
      - Disabled objects will not be deployed
    type: bool
    default: False
    choices: [True, False]
  vars:
    description:
      - Custom properties of the notification
    required: false
    type: "dict"

"""

EXAMPLES = """
- name: create notification
  t_systems_mms.icinga_director.icinga_notification:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    apply_to: host
    assign_filter: 'host.name="foohost"'
    imports:
      - foonotificationtemplate
    notification_interval: '0'
    object_name: E-Mail_host
    states:
      - Up
      - Down
    types:
      - Problem
      - Recovery
    users:
      - rb
    disabled: false
    vars:
      foo: bar
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
        imports=dict(type="list", elements="str", required=False),
        apply_to=dict(required=True, choices=["service", "host"]),
        assign_filter=dict(required=False),
        disabled=dict(
            type="bool", required=False, default=False, choices=[True, False]
        ),
        notification_interval=dict(required=False),
        states=dict(type="list", elements="str", required=False),
        users=dict(type="list", elements="str", required=False),
        types=dict(type="list", elements="str", required=False),
        vars=dict(type="dict", default={}, required=False),
    )

    # When deleting objects, only the name is necessary, so we cannot use
    # required=True in the argument_spec. Instead we define here what is
    # necessary when state is present
    required_if = [("state", "present", ["imports"])]

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
    )

    data = {
        "object_name": module.params["object_name"],
        "object_type": "apply",
        "imports": module.params["imports"],
        "apply_to": module.params["apply_to"],
        "disabled": module.params["disabled"],
        "assign_filter": module.params["assign_filter"],
        "notification_interval": module.params["notification_interval"],
        "states": module.params["states"],
        "users": module.params["users"],
        "types": module.params["types"],
        "vars": module.params["vars"],
    }

    icinga_object = Icinga2APIObject(
        module=module, path="/notification", data=data
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
