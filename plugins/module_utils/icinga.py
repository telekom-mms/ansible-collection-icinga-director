# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from collections import defaultdict

from ansible.module_utils.urls import fetch_url
from ansible.module_utils.six import iteritems
from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.parse import quote as urlquote


class Icinga2APIObject:
    module = None

    def __init__(self, module, path, data):
        self.module = module
        self.params = module.params
        self.path = path
        self.data = data
        self.object_id = None

    def call_url(self, path, data="", method="GET"):
        headers = {
            "Accept": "application/json",
            "X-HTTP-Method-Override": method,
        }
        url = self.module.params.get("url") + "/director" + path
        rsp, info = fetch_url(
            module=self.module,
            url=url,
            data=data,
            headers=headers,
            method=method,
            use_proxy=self.module.params["use_proxy"],
        )
        content = ""
        error = ""
        if rsp:
            content = json.loads(rsp.read())
        if info["status"] >= 400:
            try:
                content = json.loads(info["body"])
                error = content["error"]
            except (ValueError, KeyError):
                error = info["msg"]
        if info["status"] < 0:
            error = info["msg"]
        return {"code": info["status"], "data": content, "error": error}

    def exists(self, find_by="name"):
        ret = self.call_url(
            path=self.path
            + "?"
            + find_by
            + "="
            + to_text(urlquote(self.data["object_name"]))
        )
        self.object_id = to_text(urlquote(self.data["object_name"]))
        if ret["code"] == 200:
            return True
        return False

    def create(self):
        ret = self.call_url(
            path=self.path, data=self.module.jsonify(self.data), method="POST"
        )
        return ret

    def delete(self, find_by="name"):
        ret = self.call_url(
            path=self.path + "?" + find_by + "=" + self.object_id,
            method="DELETE",
        )
        return ret

    def modify(self, find_by="name"):
        ret = self.call_url(
            path=self.path + "?" + find_by + "=" + self.object_id,
            data=self.module.jsonify(self.data),
            method="POST",
        )
        return ret

    def scrub_diff_value(self, value):
        # /command-API gibt in den Arguments das jeweilige command_id mit, das macht die diffs unnuetz
        if isinstance(value, dict):
            for k, v in iteritems(value.copy()):
                if isinstance(value[k], dict):
                    value[k].pop("command_id", None)

        return value

    def diff(self, find_by="name"):
        ret = self.call_url(
            path=self.path + "?" + find_by + "=" + self.object_id + "&withNull",
            method="GET",
        )

        data_from_director = json.loads(self.module.jsonify(ret["data"]))
        data_from_task = json.loads(self.module.jsonify(self.data))

        diff = defaultdict(dict)
        for key, value in data_from_director.items():
            value = self.scrub_diff_value(value)
            if key in data_from_task.keys() and value != data_from_task[key]:
                diff["before"][key] = "{val}".format(val=value)
                diff["after"][key] = "{val}".format(val=data_from_task[key])

        return diff

    def update(self, state):
        changed = False
        diff_result = {"before": "", "after": ""}
        if self.exists():
            diff_result.update({"before": "state: present\n"})
            if state == "absent":
                if self.module.check_mode:
                    diff_result.update({"after": "state: absent\n"})
                    self.module.exit_json(
                        changed=True,
                        object_name=self.data["object_name"],
                        diff=diff_result,
                    )
                else:
                    try:
                        ret = self.delete()
                        if ret["code"] == 200:
                            changed = True
                            diff_result.update({"after": "state: absent\n"})
                        else:
                            self.module.fail_json(
                                msg="bad return code while deleting: %d. Error message: %s"
                                % (ret["code"], ret["error"])
                            )
                    except Exception as e:
                        self.module.fail_json(
                            msg="exception when deleting: " + str(e)
                        )

            else:
                diff_result = self.diff()
                if self.module.check_mode:
                    if diff_result:
                        changed = True
                    self.module.exit_json(
                        changed=changed,
                        object_name=self.data["object_name"],
                        data=self.data,
                        diff=diff_result,
                    )

                ret = self.modify()
                if ret["code"] == 200:
                    changed = True
                elif ret["code"] == 304:
                    changed = False
                else:
                    self.module.fail_json(
                        msg="bad return code while modifying: %d. Error message: %s"
                        % (ret["code"], ret["error"])
                    )

        else:
            diff_result.update({"before": "state: absent\n"})
            if state == "present":
                if self.module.check_mode:
                    changed = True
                    diff_result.update({"after": "state: created\n"})
                else:
                    try:
                        ret = self.create()
                        if ret["code"] == 201:
                            changed = True
                            diff_result.update({"after": "state: created\n"})
                        else:
                            self.module.fail_json(
                                msg="bad return code while creating: %d. Error message: %s"
                                % (ret["code"], ret["error"])
                            )
                    except Exception as e:
                        self.module.fail_json(
                            msg="exception while creating: " + str(e)
                        )
        return changed, diff_result
