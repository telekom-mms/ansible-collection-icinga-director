from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
name: t_systems_mms.icinga_director.icinga_director_inventory
plugin_type: inventory
short_description: Returns Ansible inventory from Icinga
description: Returns Ansible inventory from Icinga
options:
    plugin:
        description: Name of the plugin
        required: true
        choices: ['t_systems_mms.icinga_director.icinga_director_inventory']
    url:
        description: Icinga URL to connect to
        required: true
extends_documentation_fragment:
  - ansible.builtin.url
"""


from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError

from ansible.module_utils.urls import open_url
import json


class InventoryModule(BaseInventoryPlugin):
    NAME = "t_systems_mms.icinga_director.icinga_director_inventory"

    def call_url(self, url, url_username, url_password, url_path):
        """
        Execute the request against the API with the provided arguments and return json.
        """

        headers = {
            "Accept": "application/json",
            "X-HTTP-Method-Override": "GET",
        }
        url = url + url_path
        rsp = open_url(
            url,
            url_username=self.url_username,
            url_password=self.url_password,
            force_basic_auth=self.force_basic_auth,
            headers=headers,
        )
        content = ""
        if rsp:
            content = json.loads(rsp.read().decode("utf-8"))
            return content

    def verify_file(self, path):
        """Verify the configuration file."""
        if super(InventoryModule, self).verify_file(path):
            endings = (
                "icinga_director_inventory.yaml",
                "icinga_director_inventory.yml",
            )
            if any((path.endswith(ending) for ending in endings)):
                return True
        return False

    def set_hosts(self):
        host_list = self.call_url(
            self.url,
            self.url_username,
            self.url_password,
            url_path="/director/hosts",
        )

        for host in host_list["objects"]:
            self.inventory.add_host(host["object_name"])
            for item in host:
                self.inventory.set_variable(
                    host["object_name"], item, host[item]
                )

    def add_hosts_to_groups(self):
        hostgroups = self.set_hostgroups()

        for hostgroup in hostgroups:
            members = self.call_url(
                self.url,
                self.url_username,
                self.url_password,
                url_path="/monitoring/list/hosts"
                + "?hostgroup_name="
                + hostgroup
                + "&format=json",
            )
            for member in members:
                self.inventory.add_host(member["host_name"], group=hostgroup)

    def set_hostgroups(self):
        hostgroup_list = self.call_url(
            self.url,
            self.url_username,
            self.url_password,
            url_path="/director/hostgroups",
        )

        hostgroups = []

        for hostgroup in hostgroup_list["objects"]:
            hostgroups.append(hostgroup["object_name"])
            self.inventory.add_group(hostgroup["object_name"])
        return hostgroups

    def parse(self, inventory, loader, path, cache=True):
        """Return dynamic inventory from source"""

        # call base method to ensure properties are available for use with other helper methods
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        # Read the inventory YAML file
        self._read_config_data(path)

        # Store the options from the YAML file
        try:
            self.plugin = self.get_option("plugin")
            self.url = self.get_option("url")
            self.url_username = self.get_option("url_username")
            self.url_password = self.get_option("url_password")
            self.force_basic_auth = self.get_option("force_basic_auth")
        except Exception as e:
            raise AnsibleParserError("All correct options required: " + str(e))

        self.set_hosts()
        self.add_hosts_to_groups()