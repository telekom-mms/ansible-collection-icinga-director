#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 T-Systems Multimedia Solutions GmbH
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
module: icinga_job
short_description: Manage director jobs in Icinga2 Director
description:
   - Add or remove a director job in Icinga2 Director through the director API.
   - Director jobs allow scheduling automatic import and sync runs as well as other recurring tasks.
author: Michaela Mattes (@mikaEz)
extends_documentation_fragment:
  - ansible.builtin.url
  - telekom_mms.icinga_director.common_options
version_added: '2.0.0'
notes:
  - This module supports check mode.
options:
  state:
    description:
      - Apply feature state.
    choices: [ "present", "absent" ]
    default: present
    type: str
  job_name:
    description:
      - Name of the director job.
      - This must be unique across all jobs in Icinga Director.
    aliases: ['name']
    required: true
    type: str
  job_class:
    description:
      - The fully-qualified PHP class name of the job implementation.
      - Examples are C(Icinga\\Module\\Director\\Job\\ImportRunJob) to run an import source
        or C(Icinga\\Module\\Director\\Job\\SyncRunJob) to run a sync rule.
      - Required when creating a new job.
    required: false
    type: str
  disabled:
    description:
      - Whether this job is disabled and should not be run automatically.
    required: false
    type: bool
    default: false
  run_interval:
    description:
      - How often the job should run, in seconds.
      - Required when creating a new job.
    required: false
    type: int
  timeperiod:
    description:
      - The name of a time period which restricts when this job may run.
      - If not set the job may run at any time.
    required: false
    type: str
  settings:
    description:
      - A dict of job-class-specific settings stored as key-value pairs in the
        Director director_job_setting table.
      - For C(Icinga\\Module\\Director\\Job\\ImportJob) use C(source_name) to
        reference the import source by name and C(run_import) set to C("y") to
        actually run the import (default C("n") only checks for changes).
      - For C(Icinga\\Module\\Director\\Job\\SyncJob) use C(rule_name) to
        reference the sync rule by name and C(apply_changes) set to C("y") to
        actually apply changes (default C("n") only checks).
    required: false
    type: dict
    no_log: false
  append:
    description:
      - Do not overwrite the whole object but instead append the defined properties.
      - Note - Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.
      - Note - Variables that are set by default will also be applied, even if not set.
    type: bool
    choices: [true, false]
    version_added: '2.0.0'
"""

EXAMPLES = """
- name: Create a director job to run an import source
  telekom_mms.icinga_director.icinga_job:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    job_name: "Run CMDB Import"
    job_class: "Icinga\\Module\\Director\\Job\\ImportRunJob"
    run_interval: 3600
    disabled: false

- name: Create a director job to run a sync rule during business hours
  telekom_mms.icinga_director.icinga_job:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    job_name: "Run Host Sync"
    job_class: "Icinga\\Module\\Director\\Job\\SyncRunJob"
    run_interval: 900
    timeperiod: "business-hours"

- name: Disable a director job
  telekom_mms.icinga_director.icinga_job:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    job_name: "Run CMDB Import"
    disabled: true
    append: true

- name: Delete a director job
  telekom_mms.icinga_director.icinga_job:
    state: absent
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    job_name: "Run CMDB Import"
"""

RETURN = r""" # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec
from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.six.moves.urllib.parse import quote as urlquote
from ansible_collections.telekom_mms.icinga_director.plugins.module_utils.icinga import (
    Icinga2APIObject,
)


# ===========================================
# Icinga2 API class for Director Jobs.
#
class DirectorJobObject(Icinga2APIObject):
    """
    Icinga2 Director Job API object.

    Director jobs are not standard Icinga objects and use 'job_name' as their
    identifier instead of 'object_name'. This subclass adapts the base class
    to use the correct field names and API endpoints.
    """

    def exists(self):
        ret = self.call_url(
            path=self.path
            + "?name="
            + to_text(urlquote(self.data["job_name"]))
        )
        self.object_id = to_text(urlquote(self.data["job_name"]))
        return ret["code"] == 200

    def create(self):
        api_data = {k: v for k, v in self.data.items() if k != "object_name"}
        return self.call_url(
            path=self.path,
            data=self.module.jsonify(api_data),
            method="POST",
        )

    def modify(self):
        api_data = {k: v for k, v in self.data.items() if k != "object_name"}
        return self.call_url(
            path=self.path + "?name=" + self.object_id,
            data=self.module.jsonify(api_data),
            method="POST",
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
        job_name=dict(required=True, aliases=["name"]),
        job_class=dict(required=False),
        disabled=dict(type="bool", required=False, default=False),
        run_interval=dict(type="int", required=False),
        timeperiod=dict(required=False),
        settings=dict(required=False, type="dict", no_log=False),
        api_timeout=dict(required=False, default=10, type="int"),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    data_keys = [
        "job_name",
        "job_class",
        "disabled",
        "run_interval",
        "timeperiod",
    ]

    data = {}

    if module.params["append"]:
        for k in data_keys:
            if module.params[k] is not None:
                data[k] = module.params[k]
    else:
        for k in data_keys:
            data[k] = module.params[k]

    if module.params["settings"]:
        data.update(module.params["settings"])

    # Set object_name as alias for job_name to satisfy base class update()
    # during check mode. The create() and modify() overrides strip this key
    # before sending to the API.
    data["object_name"] = data["job_name"]

    icinga_object = DirectorJobObject(
        module=module, path="/job", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
