#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Ansible Project
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
module: icinga_service_template
short_description: Manage service templates in Icinga2
description:
   - "Add or remove a service template to Icinga2 through the director API."
author: Sebastian Gumprich (@rndmh3ro)
options:
  url:
    description:
      - HTTP or HTTPS URL in the form (http|https://[user[:pass]]@host.domain[:port]/path
    required: true
    type: str
  use_proxy:
    description:
      - If C(no), it will not use a proxy, even if one is defined in
        an environment variable on the target hosts.
    type: bool
    default: 'yes'
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used
        on personally controlled sites using self-signed certificates.
    type: bool
    default: 'yes'
  url_username:
    description:
      - The username for use in HTTP basic authentication.
      - This parameter can be used without C(url_password) for sites that allow empty passwords.
    type: str
  url_password:
    description:
      - The password for use in HTTP basic authentication.
      - If the C(url_username) parameter is not specified, the C(url_password) parameter will not be used.
    type: str
  force_basic_auth:
    description:
      - httplib2, the library used by the uri module only sends authentication information when a webservice
        responds to an initial request with a 401 status. Since some basic auth services do not properly
        send a 401, logins will fail. This option forces the sending of the Basic authentication header
        upon initial request.
    type: bool
    default: 'no'
  client_cert:
    description:
      - PEM formatted certificate chain file to be used for SSL client
        authentication. This file can also include the key as well, and if
        the key is included, C(client_key) is not required.
    type: path
  client_key:
    description:
      - PEM formatted file that contains your private key to be used for SSL
        client authentication. If C(client_cert) contains both the certificate
        and key, this option is not required.
    type: path
  state:
    description:
      - Apply feature state.
    choices: [ "present", "absent" ]
    default: present
    type: str
  object_name:
    description:
      - Name of the service template
    required: true
    type: str
  check_command:
    description:
      - Check command definition
    required: false
    type: str
  check_interval:
    description:
      - Your regular check interval
    required: false
    type: str
  check_period:
    description:
      - The name of a time period which determines when this object should be monitored. Not limited by default.
    required: false
    type: str
  check_timeout:
    description:
      - Check command timeout in seconds. Overrides the CheckCommand's timeout attribute
    required: false
    type: str
  enable_active_checks:
    description:
      - Whether to actively check this object
    required: false
    type: "bool"
  enable_event_handler:
    description:
      - Whether to enable event handlers this object
    required: false
    type: "bool"
  enable_notifications:
    description:
      - Whether to send notifications for this object
    required: false
    type: "bool"
  enable_passive_checks:
    description:
      - Whether to accept passive check results for this object
    required: false
    type: "bool"
  enable_perfdata:
    description:
      - Whether to process performance data provided by this object
    required: false
    type: "bool"
  groups:
    description:
      - Service groups that should be directly assigned to this service.
        Servicegroups can be useful for various reasons.
        They are helpful to provided service-type specific view in Icinga Web 2, either for custom dashboards
        or as an instrument to enforce restrictions.
        Service groups can be directly assigned to single services or to service templates.
    required: false
    type: "list"
    elements: "str"
    default: []
  imports:
    description:
      - Importable templates, add as many as you want.
        Please note that order matters when importing properties from multiple templates - last one wins
    required: false
    type: "list"
    elements: "str"
    default: []
  max_check_attempts:
    description:
      - Defines after how many check attempts a new hard state is reached
    required: false
    type: str
  notes:
    description:
      - Additional notes for this object
    required: false
    type: str
  retry_interval:
    description:
      - Retry interval, will be applied after a state change unless the next hard state is reached
    required: false
    type: str
  use_agent:
    description:
      - Whether the check commmand for this service should be executed on the Icinga agent
    required: false
    type: "bool"
  vars:
    description:
      - Custom properties of the template
    required: false
    type: "dict"
    default: {}
  volatile:
    description:
      - Whether this check is volatile.
    required: false
    type: "bool"
  disabled:
    description:
      - Disabled objects will not be deployed
    type: bool
    default: False
    choices: [True, False]
"""

EXAMPLES = """
- name: create servicetemplate
  tags: servicetemplate
  icinga_service_template:
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    object_name: fooservicetemplate
    use_agent: true
    vars:
      procs_argument: consul
      procs_critical: '1:'
      procs_warning: '1:'
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
        groups=dict(type="list", elements="str", default=[], required=False),
        imports=dict(type="list", elements="str", default=[], required=False),
        max_check_attempts=dict(required=False),
        notes=dict(required=False),
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
        "object_type": "template",
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
        "imports": module.params["imports"],
        "max_check_attempts": module.params["max_check_attempts"],
        "notes": module.params["notes"],
        "retry_interval": module.params["retry_interval"],
        "use_agent": module.params["use_agent"],
        "vars": module.params["vars"],
        "volatile": module.params["volatile"],
    }

    try:
        icinga_object = Icinga2APIObject(
            module=module, path="/service", data=data
        )
    except Exception as e:
        module.fail_json(
            msg="unable to connect to Icinga. Exception message: %s" % e
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
