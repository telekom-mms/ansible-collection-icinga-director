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
module: icinga_command_template
short_description: Manage command templates in Icinga2
description:
   - Add or remove a command template to Icinga2 through the director API.
author: Lars Krahl (@mmslkr)
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
version_added: '1.1.0'
notes:
  - This module supports check mode.
deprecated:
  why: moved collection to new organisation telekom_mms
  removed_in: 3.0.0
  alternative: telekom_mms.icinga_director.icinga_command_template
options:
  state:
    description:
      - Apply feature state.
    choices: [ "present", "absent" ]
    default: present
    type: str
  command:
    description:
      - The command Icinga should run.
      - Absolute paths are accepted as provided, relative paths are prefixed with "PluginDir + ", similar Constant prefixes are allowed.
      - Spaces will lead to separation of command path and standalone arguments.
      - Please note that this means that we do not support spaces in plugin names and paths right now.
    type: str
  methods_execute:
    description:
      - Plugin Check commands are what you need when running checks against your infrastructure.
      - Notification commands will be used when it comes to notify your users.
      - Event commands allow you to trigger specific actions when problems occur.
      - Some people use them for auto-healing mechanisms, like restarting services or rebooting systems at specific thresholds.
    choices: ["PluginCheck", "PluginNotification", "PluginEvent"]
    default: "PluginCheck"
    aliases: ['command_type']
    type: str
  disabled:
    description:
      - Disabled objects will not be deployed.
    type: bool
    default: false
    choices: [true, false]
  object_name:
    description:
      - Name of the command template.
    aliases: ['name']
    required: true
    type: str
  imports:
    description:
      - Importable templates, add as many as you want. Please note that order matters when importing properties from multiple templates - last one wins.
    type: list
    elements: str
    default: []
  timeout:
    description:
      - Optional command timeout. Allowed values are seconds or durations postfixed with a specific unit (for example 1m or also 3m 30s).
    type: str
  zone:
    description:
      - Icinga cluster zone. Allows to manually override Directors decisions of where to deploy your config to.
      - You should consider not doing so unless you gained deep understanding of how an Icinga Cluster stack works.
    type: str
  vars:
    description:
      - Custom properties of the command template.
    type: "dict"
    default: {}
  arguments:
    description:
      - Arguments of the command template.
      - Each argument can take either a string, a json or a dict
      - When using a dict as argument value, the following properties are supported.
        C(skip_key), C(repeat_key), C(required), C(order), C(description)),
        C(set_if), C(value).
      - The C(value) property can be either a string, a json or a dict. When used as a dict, you can define
        its C(type) as C(Function) and set its C(body) property as an Icinga DSL piece of config.
    type: "dict"
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
- name: Create command template
  t_systems_mms.icinga_director.icinga_command_template:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    arguments:
      '--authpassphrase':
        value: $snmpv3_priv_key$
      '--authprotocol':
        value: $snmpv3_auth_protocol$
      '--critical':
        value: $centreon_critical$
      '--filter':
        value: $centreon_filter$
      '--hostname':
        value: $snmp_address$
      '--maxrepetitions':
        value: $centreon_maxrepetitions$
      '--mode':
        value: $centreon_mode$
      '--plugin':
        value: $centreon_plugin$
      '--privpassphrase':
        value: $snmpv3_auth_key$
      '--privprotocol':
        value: $snmpv3_priv_protocol$
      '--snmp-community':
        value: $snmp_community$
      '--snmp-timeout':
        value: $snmp_timeout$
      '--snmp-username':
        value: $snmpv3_user$
      '--snmp-version':
        value: $snmp_version$
      '--subsetleef':
        value: $centreon_subsetleef$
      '--verbose':
        set_if: $centreon_verbose$
      '--warning':
        value: $centreon_warning$
      '--dummy-arg':
        description: "dummy arg using Icinga DSL code"
        value:
          type: "Function"
          body: 'return macro("$dummy_var$")'
    command: "/opt/centreon-plugins/centreon_plugins.pl"
    command_type: "PluginCheck"
    object_name: centreon-plugins-template
    disabled: false
    vars:
      centreon_maxrepetitions: 20
      centreon_subsetleef: 20
      centreon_verbose: false
      snmp_address: $address$
      snmp_timeout: 60
      snmp_version: '2'
      snmpv3_auth_key: authkey
      snmpv3_priv_key: privkey
      snmpv3_user: user

- name: Update command template
  t_systems_mms.icinga_director.icinga_command_template:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: centreon-plugins-template
    timeout: "2m"
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
        imports=dict(type="list", elements="str", required=False, default=[]),
        disabled=dict(
            type="bool", required=False, default=False, choices=[True, False]
        ),
        vars=dict(type="dict", default={}),
        command=dict(required=False),
        methods_execute=dict(
            default="PluginCheck",
            choices=["PluginCheck", "PluginNotification", "PluginEvent"],
            aliases=["command_type"],
        ),
        timeout=dict(required=False, default=None),
        zone=dict(required=False, default=None),
        arguments=dict(type="dict", default=None),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    # `arguments` is of type dict, default should be {}
    # however, the director api returns [] when no `arguments` are set, making the diff seem changed
    # therefore set the default to [] as well to get a clean diff output
    if not module.params["arguments"]:
        module.params["arguments"] = []

    data_keys = [
        "object_name",
        "imports",
        "disabled",
        "vars",
        "command",
        "methods_execute",
        "timeout",
        "zone",
        "arguments",
    ]

    data = {}

    if module.params["append"]:
        for k in data_keys:
            if module.params[k]:
                data[k] = module.params[k]
    else:
        for k in data_keys:
            data[k] = module.params[k]

    data["object_type"] = "template"

    icinga_object = Icinga2APIObject(module=module, path="/command", data=data)

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
