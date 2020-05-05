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
module: icinga_service_apply
short_description: Manage service apply rules in Icinga2
description:
   - "Add or remove a service apply rule to Icinga2 through the director API."
author: "Sebastian Gumprich"
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
      - Name for the Icinga service you are going to create
    required: true
    type: str
  display_name:
    description:
      - Alternative displayed name of the service apply rule
    required: false
    type: str
  groups:
    description:
      - Service groups that should be directly assigned to this service.
        Servicegroups can be useful for various reasons.
        They are helpful to provided service-type specific view in Icinga Web 2, either for custom dashboards
        or as an instrument to enforce restrictions.
        Service groups can be directly assigned to single services or to service templates.
    required: false
    type: "list"
  apply_for:
    description:
      - Evaluates the apply for rule for all objects with the custom attribute specified.
        E.g selecting "host.vars.custom_attr" will generate "for (config in host.vars.array_var)" where "config"
        will be accessible through "$config$". NOTE - only custom variables of type "Array" are eligible.
    required: false
    type: str
  assign_filter:
    description:
      - The filter where the service apply rule will take effect
    required: false
    type: str
  imports:
    description:
      - Importable templates, add as many as you want.
        Please note that order matters when importing properties from multiple templates - last one wins
    required: false
    type: "list"
  vars:
    description:
      - Custom properties of the host
    required: false
    type: "dict"
  notes:
    description:
      - Additional notes for this object
    required: false
    type: str
  notes_url:
    description:
      - An URL pointing to additional notes for this object.
      - Separate multiple urls like this "'http://url1' 'http://url2'".
      - Max length 255 characters
    required: false
    type: str
'''

EXAMPLES = '''
- name: Add service apply rule to icinga
  icinga_service_apply:
    state: present
    url: "https://example.com"
    url_username: ""
    url_password: ""
    object_name: "SERVICE_promtail"
    assign_filter: 'host.vars.HostOS="Linux"&host.name="sbk-pilot-api*'
    apply_for: "host.vars.enabled_notifications"
    display_name: "Promtail process"
    imports:
      - http
    groups:
      - sbk
    vars:
      http_address: "$address$"
      http_port: "9080"
      http_uri: "/ready"
      http_string: "Ready"
      http_expect: "Yes"
'''

import json
from collections import defaultdict

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
from ansible_collections.T_Systems_MMS.icinga.plugins.module_utils.icinga import Icinga2APIObject


# ===========================================
# Icinga2 API class
#
class ServiceApplyRule(Icinga2APIObject):

    def __init__(self, module, data):
        path = '/service'
        super(ServiceApplyRule, self).__init__(module, path, data)

    def exists(self):
        ret = self.call_url(
            path="/serviceapplyrules",
        )
        if ret['code'] == 200:
            for existing_rule in ret['data']['objects']:
                if existing_rule['object_name'] == self.data['object_name']:
                    self.object_id = existing_rule['id']
                    return self.object_id
        return False

    def delete(self):
        return super(ServiceApplyRule, self).delete(find_by='id')

    def modify(self):
        return super(ServiceApplyRule, self).modify(find_by='id')

    def diff(self):
        return super(ServiceApplyRule, self).diff(find_by='id')


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
        display_name=dict(required=True),
        apply_for=dict(required=False),
        assign_filter=dict(required=False),
        imports=dict(type='list', required=False),
        groups=dict(type='list', default=[], required=False),
        vars=dict(type='dict', default={}),
        notes=dict(type='str', required=False),
        notes_url=dict(type='str', required=False),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    state = module.params["state"]
    object_name = module.params["object_name"]
    display_name = module.params["display_name"]
    apply_for = module.params["apply_for"]
    assign_filter = module.params["assign_filter"]
    imports = module.params["imports"]
    groups = module.params["groups"]
    vars = module.params["vars"]
    notes = module.params["notes"]
    notes_url = module.params["notes_url"]

    data = {
        'object_name': object_name,
        'display_name': display_name,
        'object_type': "apply",
        'apply_for': apply_for,
        'assign_filter': assign_filter,
        'imports': imports,
        'groups': groups,
        'vars': vars,
        'notes': notes,
        'notes_url': notes_url,
    }

    try:
        icinga_object = ServiceApplyRule(module=module, data=data)
    except Exception as e:
        module.fail_json(msg="unable to connect to Icinga. Exception message: %s" % e)

    changed, diff = icinga_object.update(state)
    module.exit_json(changed=changed, object_name=object_name, data=icinga_object.data, diff=diff)


# import module snippets
if __name__ == '__main__':
    main()
