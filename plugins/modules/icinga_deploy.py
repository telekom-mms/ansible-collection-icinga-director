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
module: icinga_deploy
short_description: Trigger deployment in Icinga2
description:
  - Trigger a deployment to Icinga2 through the director API.
author: Falk Händler (@flkhndlr)
version_added: '1.33.0'
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
notes:
  - This module supports check mode.
"""

EXAMPLES = """
- name: Deploy the icinga config
  t_systems_mms.icinga_director.icinga_deploy:
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
  register: result

"""

RETURN = r""" # """

from ansible.module_utils.urls import url_argument_spec
from  ansible.module_utils.basic import AnsibleModule
from ansible_collections.t_systems_mms.icinga_director.plugins.module_utils.icinga import (
    Icinga2APIObject,
)


# ===========================================
# Icinga2 API class
#

class Deployment(Icinga2APIObject):
    
    def query(self, find_by="checksum"):
        return super(Deployment, self).exists(find_by)
    
    def create(self):
        return super(Deployment, self).create()
    


# ===========================================
# Module execution.
#
def main():
    # use the predefined argument spec for url
    argument_spec = url_argument_spec()
    
    # add our own arguments
    argument_spec.update(
        address=dict(required=False),
        address6=dict(required=False),
        url=dict(required=True),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    icinga_object = Deployment(module=module, path="/config/deploy", data=[])
    
    result = icinga_object.create()

    module.exit_json(
        result=result,
    )

if __name__ == "__main__":
    main()
