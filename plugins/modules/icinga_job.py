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
  - Uses the standard C(/director/jobs) bulk endpoint (GET/POST/DELETE).
    Requires Director with upstream PR adding POST and DELETE support to
    C(JobsController) and C(unserializeJobs) in C(ImportExport).
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
    job_class: Icinga\\Module\\Director\\Job\\ImportRunJob
    run_interval: 3600
    disabled: false

- name: Create a director job to run a sync rule during business hours
  telekom_mms.icinga_director.icinga_job:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    job_name: "Run Host Sync"
    job_class: Icinga\\Module\\Director\\Job\\SyncRunJob
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

    Uses the standard /director/jobs (plural) bulk endpoint, available in
    Director >= 1.3 once the upstream PR adding POST/DELETE support has been
    merged.  This avoids any patched singular controller.

    Behaviour mirrors icinga_importsource:
      exists()  – GET /director/jobs, search list by job_name
      create()  – POST single-element array to /director/jobs
      modify()  – same POST (unserialize is idempotent / upsert)
      delete()  – DELETE /director/jobs?name=<job_name>
    """

    _BULK_KEYS = frozenset([
        "job_name", "job_class", "disabled", "run_interval", "timeperiod", "settings",
    ])

    def __init__(self, module, path, data):
        super().__init__(module, path, data)
        self._current = None  # populated by exists()

    def _desired_payload(self):
        """Build a single job object in the Director bulk export format."""
        current = self._current or {}
        append = self.data.get("_append", False)

        def _val(key):
            v = self.data.get(key)
            if v is None and append:
                return current.get(key)
            return v

        # Director stores disabled as "y"/"n"; convert Python bool
        disabled = _val("disabled")
        if isinstance(disabled, bool):
            disabled = "y" if disabled else "n"

        # Merge settings dict in append mode
        settings = self.data.get("settings") or {}
        if append:
            merged = dict(current.get("settings") or {})
            merged.update(settings)
            settings = merged

        payload = {
            "job_name": self.data["job_name"],
            "job_class": _val("job_class"),
            "disabled": disabled,
            # Director stores and returns run_interval as a string — normalise
            # to str here so that modify() comparison matches without extra logic.
            "run_interval": str(_val("run_interval")) if _val("run_interval") is not None else None,
            "settings": settings,
        }
        # timeperiod uses a special setter in Director (setTimeperiod) that
        # throws InvalidArgumentException when passed null.  Only include it
        # when explicitly set so ObjectImporter does not call setTimeperiod(null).
        tp = _val("timeperiod")
        if tp is not None:
            payload["timeperiod"] = tp
        return payload

    def exists(self):
        """Check if the job exists.

        Tries the bulk endpoint GET /director/jobs first (requires
        icingaweb2-module-otc patch on Director).  Falls back to the
        standard singular endpoint GET /director/job?name=<name> so that
        the module also works against an unpatched Director.
        """
        name = self.data["job_name"]
        self.object_id = to_text(urlquote(name))

        # Try bulk endpoint (available when icingaweb2-module-otc patch is applied)
        ret = self.call_url(path=self.path)
        if ret["code"] == 200:
            jobs = ret["data"] if isinstance(ret["data"], list) else []
            for job in jobs:
                if job.get("job_name") == name:
                    self._current = job
                    return True
            self._current = None
            return False

        # Fall back to singular endpoint (standard Director API, always available)
        ret = self.call_url(path="/job?name=" + self.object_id)
        if ret["code"] == 200:
            self._current = ret["data"] if isinstance(ret["data"], dict) else {}
            return True
        self._current = None
        return False

    def create(self):
        """POST single-element array to /director/jobs."""
        ret = self.call_url(
            path=self.path,
            data=self.module.jsonify([self._desired_payload()]),
            method="POST",
        )
        # Bulk endpoint returns HTTP 200 on success; translate to 201 so that
        # the base update() method treats the result as "created".
        if ret["code"] == 200:
            ret["code"] = 201
        return ret

    @staticmethod
    def _norm(val):
        """Normalize Director boolean variants (True/"y" and False/"n"/None) for comparison."""
        if val is True or val == "y":
            return "y"
        if val is False or val == "n" or val is None:
            return "n"
        return val

    def modify(self):
        """POST only when the desired state differs from the current state."""
        desired = self._desired_payload()
        current = self._current or {}
        if all(self._norm(current.get(k)) == self._norm(desired.get(k)) for k in self._BULK_KEYS):
            return {"code": 304, "data": {}, "error": ""}
        return self.call_url(
            path=self.path,
            data=self.module.jsonify([desired]),
            method="POST",
        )

    def diff(self, find_by="name"):
        """Return a before/after diff dict for changed _BULK_KEYS only."""
        current = self._current or {}
        desired = self._desired_payload()
        before, after = {}, {}
        for key in self._BULK_KEYS:
            cv, dv = current.get(key), desired.get(key)
            if self._norm(cv) != self._norm(dv):
                before[key] = cv
                after[key] = dv
        return {"before": before, "after": after} if before else {}

    def delete(self, find_by="name"):
        """DELETE the job.

        Uses the standard singular endpoint DELETE /director/job?name=<name>
        which is always available in Director without any patches.
        """
        return self.call_url(
            path="/job?name=" + self.object_id,
            method="DELETE",
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
        data["_append"] = True
        for k in data_keys:
            if module.params[k] is not None:
                data[k] = module.params[k]
    else:
        for k in data_keys:
            data[k] = module.params[k]

    # Keep settings as a nested dict (bulk format); do not merge into data
    if module.params["settings"] is not None:
        data["settings"] = module.params["settings"]
    else:
        data["settings"] = {}

    # object_name is required by the base class update() / check-mode path
    data["object_name"] = data["job_name"]

    icinga_object = DirectorJobObject(
        module=module, path="/jobs", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
