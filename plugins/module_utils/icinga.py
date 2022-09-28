# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from collections import defaultdict

from ansible.module_utils.urls import fetch_url
from ansible.module_utils.six import iteritems
from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.six.moves.urllib.parse import quote as urlquote


class Icinga2APIObject(object):
    """Interact with the icinga2 director API"""

    module = None

    def __init__(self, module, path, data):
        self.module = module
        self.params = module.params
        self.path = path
        self.data = data
        self.object_id = None

    def call_url(self, path, data="", method="GET"):
        """
        Execute the request against the API with the provided arguments and return json.

        Parameters:
            path: type str, the path of the api to call
            data: type str, the module params passed to the api
            method: type str, default "GET", the method to run against the api.
                    GET to check objects, POST to create or modify objects, DELETE to delete objects

        Returns:
            jsonString with return code, the resulting data from the api-call and errors if there are any
        """

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

        # handle 400 errors
        if info["status"] >= 400:
            try:
                content = json.loads(info["body"].decode("utf-8"))
                error = content["error"]
            except (ValueError, KeyError):
                error = info["msg"]

        # handle other errors
        elif info["status"] < 0:
            error = info["msg"]

        # if nothing is modified when trying to change objects, fetch_url
        # returns only the 304 status but no body.
        # if that happens we set the content to an empty json object.
        # else we serialize the response as a json object.
        elif info["status"] == 304:
            content = {}
        else:
            content = json.loads(rsp.read().decode("utf-8"))

        return {"code": info["status"], "data": content, "error": error}

    def exists(self, find_by="name"):
        """
        Check if the object already exists in the director.

        Parameters:
            find_by: type str, default "name", the object key to search for. by default 'name' of the object,
                     however service apply rules have no name and have to be found by their id.
        Returns:
            boolean that tells wether the object exists
        """

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

    def query(self, query="", resolved=False):
        """
        Find all matching objects in the director and return the result of the api-call.

        Parameters:
            query: type str, default "", searchstring to limit the results. By default Director will search in
                   the name of the resource. Usually that means 'object_name', but for services it also covers
                   the host name.
            resolved: type bool, default False, resolve all object variables. If True, this will include all
                      variables inherited via imports.

        Returns:
            the result of the api-call
        """

        try:
            ret = self.call_url(
                path=self.path
                + "?q="
                + to_text(urlquote(query))
                + ("&resolved" if resolved else "")
            )
            if ret["code"] != 200:
                self.module.fail_json(
                    msg="bad return code while querying: %d. Error message: %s"
                    % (ret["code"], ret["error"])
                )
        except Exception as e:
            self.module.fail_json(msg="exception when querying: " + str(e))

        return ret

    def create(self):
        """
        Create the object in the director and return the result of the api-call.

        Parameters:
            none

        Returns:
            the result of the api-call
        """

        ret = self.call_url(
            path=self.path, data=self.module.jsonify(self.data), method="POST"
        )
        return ret

    def delete(self, find_by="name"):
        """
        Delete the object in the director and return the result of the api-call.

        Parameters:
            find_by: type str, default "name", the object key to search for. by default 'name' of the object,
                     however service apply rules have no name and have to be found by their id.
        Returns:
            the result of the api-call
        """

        ret = self.call_url(
            path=self.path + "?" + find_by + "=" + self.object_id,
            method="DELETE",
        )
        return ret

    def modify(self, find_by="name"):
        """
        Modify the object in the director and return the result of the api-call.

        Parameters:
            find_by: type str, default "name", the object key to search for. by default 'name' of the object,
                     however service apply rules have no name and have to be found by their id.
        Returns:
            the result of the api-call
        """

        ret = self.call_url(
            path=self.path + "?" + find_by + "=" + self.object_id,
            data=self.module.jsonify(self.data),
            method="POST",
        )
        return ret

    def scrub_diff_value(self, value):
        """
        Scrub the 'command_id' key from the returned data.

        The command api returns the command_id, rendering the diff useless

        Parameters:
            value: type dict, the dict to remove the command_id key from

        Returns:
            the dict value without the key command_id
        """

        if isinstance(value, dict):
            for k, v in iteritems(value.copy()):
                if isinstance(value[k], dict):
                    value[k].pop("command_id", None)

        return value

    def diff(self, find_by="name"):
        """
        Produce the diff for the changed object and return it.

        Parameters:
            find_by: type str, default "name", the object key to search for. by default 'name' of the object,
                     however service apply rules have no name and have to be found by their id.

        Returns:
            the generated diff
        """

        ret = self.call_url(
            path=self.path + "?" + find_by + "=" + self.object_id + "&withNull",
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
        """
        Create, update or delete the objects in the director.

        Parameters:
            state: type str, the state of the object, present or absent

        Returns:
            changed: wether the object was changed
            diff_result: the diff of the object
        """

        changed = False
        diff_result = {"before": "", "after": ""}

        try:
            exists = self.exists()
        except Exception as e:
            self.module.fail_json(msg="exception when deleting: " + str(e))
        if exists:
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
                try:
                    diff_result = self.diff()
                except Exception as e:
                    self.module.fail_json(
                        msg="exception when diffing: " + str(e)
                    )

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
