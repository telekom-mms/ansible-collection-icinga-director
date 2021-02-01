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
module: icinga_command
short_description: Manage commands in Icinga2
description:
   - Add or remove a command to Icinga2 through the director API.
author: Sebastian Gumprich (@rndmh3ro)
version_added: '1.0.0'
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
notes:
  - This module supports check mode.
options:
  state:
    description:
      - Apply feature state.
    choices: [ "present", "absent" ]
    default: present
    type: str
  command:
    description:
      - The command Icinga should run. Required when state is C(present).
      - Absolute paths are accepted as provided, relative paths are prefixed with "PluginDir + ", similar Constant prefixes are allowed.
      - Spaces will lead to separation of command path and standalone arguments.
      - Please note that this means that we do not support spaces in plugin names and paths right now.
    type: str
  command_type:
    description:
      - Plugin Check commands are what you need when running checks against your infrastructure.
      - Notification commands will be used when it comes to notify your users.
      - Event commands allow you to trigger specific actions when problems occur.
      - Some people use them for auto-healing mechanisms, like restarting services or rebooting systems at specific thresholds.
    choices: ["PluginCheck", "PluginNotification", "PluginEvent"]
    default: "PluginCheck"
    type: str
  disabled:
    description:
      - Disabled objects will not be deployed.
    type: bool
    default: False
    choices: [True, False]
  object_name:
    description:
      - Name of the command.
    aliases: ['name']
    required: true
    type: str
  imports:
    description:
      - Importable templates, add as many as you want. Please note that order matters when importing properties from multiple templates - last one wins.
    type: list
    elements: str
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
      - Custom properties of the command.
    type: "dict"
  arguments:
    description:
      - Arguments of the command.
    type: "dict"
"""

EXAMPLES = """
- name: Create command
  t_systems_mms.icinga_director.icinga_command:
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
    command: "/opt/centreon-plugins/centreon_plugins.pl"
    command_type: "PluginCheck"
    disabled: false
    object_name: centreon-plugins
    imports:
      - centreon-plugins-template
    timeout: "1m"
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

- name: Create command
  t_systems_mms.icinga_director.icinga_command:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    command: "/opt/centreon-plugins/centreon_plugins_2.pl"
    object_name: centreon-plugins_2

- name: Create event command
  t_systems_mms.icinga_director.icinga_command:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    command: "/opt/scripts/restart_httpd"
    object_name: "restart_httpd"
    arguments:
      '-s':
        value: $service.state$
      '-t':
        value: $service.state_type$
      '-a':
        set_if: $service.check_attempt$
        value: $restart_service$
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
        object_name=dict(required=True, aliases=["name"]),
        imports=dict(type="list", elements="str", required=False, default=[]),
        disabled=dict(
            type="bool", required=False, default=False, choices=[True, False]
        ),
        vars=dict(type="dict", default={}),
        command=dict(required=False),
        command_type=dict(
            default="PluginCheck",
            choices=["PluginCheck", "PluginNotification", "PluginEvent"],
        ),
        timeout=dict(required=False, default=None),
        zone=dict(required=False, default=None),
        arguments=dict(type="dict", default=None),
    )

    # When deleting objects, only the name is necessary, so we cannot use
    # required=True in the argument_spec. Instead we define here what is
    # necessary when state is present
    required_if = [("state", "present", ["object_name"])]

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
    )

    # typ von arguments ist eigentlich dict, also ohne Angabe = {}
    # die director API schickt hier aber ein leeres Array zurueck wenn nichts definiert
    # daher ueberschreiben, damit der diff besser funktioniert
    if not module.params["arguments"]:
        module.params["arguments"] = []

    data = {
        "object_name": module.params["object_name"],
        "object_type": "object",
        "imports": module.params["imports"],
        "disabled": module.params["disabled"],
        "vars": module.params["vars"],
        "command": module.params["command"],
        "methods_execute": module.params["command_type"],
        "timeout": module.params["timeout"],
        "zone": module.params["zone"],
        "arguments": module.params["arguments"],
    }

    icinga_object = Icinga2APIObject(module=module, path="/command", data=data)

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
