# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Ansible Project
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


class ModuleDocFragment(object):
    # Documentation for authentication options that are always the same
    DOCUMENTATION = r"""
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
    """
