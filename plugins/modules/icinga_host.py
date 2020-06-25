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
module: icinga_host
short_description: Manage hosts in Icinga2
description:
   - "Add or remove a host to Icinga2 through the director API."
author:
  - "Sebastian Gumprich"
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
      - Icinga object name for this host.
        This is usually a fully qualified host name but it could basically be any kind of string.
        To make things easier for your users we strongly suggest to use meaningful names for templates.
        E.g. "generic-host" is ugly, "Standard Linux Server" is easier to understand
    required: true
    type: str
  display_name:
    description:
      - Alternative name for this host.
        Might be a host alias or and kind of string helping your users to identify this host
    required: false
    type: str
  address:
    description:
      - Host address. Usually an IPv4 address, but may be any kind of address your check plugin is able to deal with
    required: false
    type: str
  groups:
    description:
      - Hostgroups that should be directly assigned to this node. Hostgroups can be useful for various reasons.
        You might assign service checks based on assigned hostgroup. They are also often used as an instrument to
        enforce restricted views in Icinga Web 2.
        Hostgroups can be directly assigned to single hosts or to host templates.
        You might also want to consider assigning hostgroups using apply rules
    required: false
    type: list
    default: []
  disabled:
    description:
      - Disabled objects will not be deployed
    required: False
    default: False
    type: bool
    choices: [True, False]
  imports:
    description:
      - Choose a Host Template
    required: true
    type: list
  zone:
    description:
      - Set the zone
    required: false
    type: str
  vars:
    description:
      - Custom properties of the host
    required: false
    type: "dict"
  check_command:
    description:
      - The name of the check command. Though this is not required to be defined in the director,
        you still have to supply a check_command in a host or host-template
    required: false
    type: str
"""

EXAMPLES = """
- name: create a host in icinga
  icinga_host:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    disabled: false
    object_name: "foohost"
    address: "127.0.0.1"
    display_name: "foohost"
    groups:
      - "foohostgroup"
    imports:
      - "foohosttemplate"
    vars:
      dnscheck: "no"
    check_command: dummy
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
        object_name=dict(required=True),
        display_name=dict(required=False),
        groups=dict(type="list", default=[], required=False),
        imports=dict(type="list", required=True),
        disabled=dict(type="bool", default=False, choices=[True, False]),
        address=dict(required=False),
        zone=dict(required=False, default=None),
        vars=dict(type="dict", default=None),
        check_command=dict(required=False),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    data = {
        "object_name": module.params["object_name"],
        "object_type": "object",
        "display_name": module.params["display_name"],
        "groups": module.params["groups"],
        "imports": module.params["imports"],
        "disabled": module.params["disabled"],
        "address": module.params["address"],
        "zone": module.params["zone"],
        "vars": module.params["vars"],
        "check_command": module.params["check_command"],
    }

    try:
        icinga_object = Icinga2APIObject(module=module, path="/host", data=data)
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
