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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: icinga_user_template
short_description: Manage user templates in Icinga2
description:
   - "Add or remove a user template to Icinga2 through the director API."
author: "Lars Krahl"
options:
  url:
    description:
      - HTTP, HTTPS, or FTP URL in the form (http|https|ftp)://[user[:pass]]@host.domain[:port]/path
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
      - Name of the user template
    required: true
    type: str
  imports:
    description:
      - Importable templates, add as many as you want. Please note that order matters when importing properties from multiple templates - last one wins
    required: false
    type: list
  period:
    description:
      - The name of a time period which determines when notifications to this User should be triggered. Not set by default.
    required: false
    type: str
  enable_notifications:
    description:
      - Whether to send notifications for this user
    type: bool
'''

EXAMPLES = '''
  - name: create user template
    icinga_user_template:
      state: present
      url: "https://example.com"
      url_username: "{{ icinga_user }}"
      url_password: "{{ icinga_pass }}"
      object_name: "a_user_template"
      enable_notifications: true
      period: '24/7'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec
from ansible_collections.T_Systems_MMS.icinga.plugins.module_utils.icinga import Icinga2APIObject


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
        imports=dict(type='list', default=[], required=False),
        period=dict(required=False),
        enable_notifications=dict(type="bool", required=False),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    state = module.params["state"]
    object_name = module.params["object_name"]
    imports = module.params["imports"]
    period = module.params["period"]
    enable_notifications = module.params["enable_notifications"]

    data = {
        'object_name': object_name,
        'object_type': "template",
        'imports': imports,
        'period': period,
        'enable_notifications': enable_notifications,
    }

    try:
        icinga_object = Icinga2APIObject(module=module, path="/user", data=data)
    except Exception as e:
        module.fail_json(msg="unable to connect to Icinga. Exception message: %s" % e)

    changed, diff = icinga_object.update(state)
    module.exit_json(changed=changed, object_name=object_name, data=icinga_object.data, diff=diff)


# import module snippets
if __name__ == '__main__':
    main()
