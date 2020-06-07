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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: icinga_hostgroup
short_description: Manage hostgroups in Icinga2
description:
   - "Add or remove a hostgroup to Icinga2 through the director API."
author: "Sebastian Gumprich"
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
      - Icinga object name for this hostgroup.
    required: true
    type: str
  display_name:
    description:
      - An alternative display name for this group.
        If you wonder how this could be helpful just leave it blank
    required: false
    type: str
  assign_filter:
    description:
      - This allows you to configure an assignment filter.
         Please feel free to combine as many nested operators as you want
    required: false
    type: str
'''

EXAMPLES = '''
  - name: create hostgroup
    icinga_hostgroup:
      state: present
      url: "https://example.com"
      url_username: "{{ icinga_user }}"
      url_password: "{{ icinga_pass }}"
      object_name: customer-hostgroup
      assign_filter: 'host.name="cust-*"'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec
from ansible_collections.t_systems_mms.icinga_director.plugins.module_utils.icinga import Icinga2APIObject


# ===========================================
# Module execution.
#


def main():
    # use the predefined argument spec for url
    argument_spec = url_argument_spec()
    # remove unnecessary argument 'force'
    del argument_spec['force']
    del argument_spec['http_agent']
    # add our own arguments
    argument_spec.update(
        state=dict(default="present", choices=["absent", "present"]),
        object_name=dict(required=True),
        display_name=dict(required=False),
        assign_filter=dict(required=False),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    state = module.params["state"]
    object_name = module.params["object_name"]
    display_name = module.params["display_name"]
    assign_filter = module.params["assign_filter"]

    data = {
        'object_name': object_name,
        'object_type': "object",
        'display_name': display_name,
        'assign_filter': assign_filter,
    }

    try:
        icinga_object = Icinga2APIObject(module=module, path="/hostgroup", data=data)
    except Exception as e:
        module.fail_json(msg="unable to connect to Icinga. Exception message: %s" % e)

    changed, diff = icinga_object.update(state)
    module.exit_json(changed=changed, object_name=object_name, data=icinga_object.data, diff=diff)


# import module snippets
if __name__ == '__main__':
    main()
