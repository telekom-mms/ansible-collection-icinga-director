.. _icinga_endpoint_module:


icinga_endpoint -- Manage endpoints in Icinga2
==============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove an endpoint to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  object_name (True, str, None)
    Icinga object name for this endpoint.

    This is usually a fully qualified host name but it could basically be any kind of string.

    To make things easier for your users we strongly suggest to use meaningful names for templates.

    For example "generic-endpoint" is ugly, "Standard Linux Server" is easier to understand.


  host (optional, str, None)
    The hostname/IP address of the remote Icinga 2 instance.


  port (optional, int, None)
    The service name/port of the remote Icinga 2 instance. Defaults to 5665.


  log_duration (optional, str, None)
    Duration for keeping replay logs on connection loss. Defaults to 1d (86400 seconds). Attribute is specified in seconds. If log_duration is set to 0, replaying logs is disabled. You could also specify the value in human readable format like 10m for 10 minutes or 1h for one hour.


  zone (optional, str, None)
    The name of the zone this endpoint is part of.


  append (optional, bool, None)
    Do not overwrite the whole object but instead append the defined properties.

    Note - Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.

    Note - Variables that are set by default will also be applied, even if not set.


  url (True, str, None)
    HTTP, HTTPS, or FTP URL in the form (http|https|ftp)://[user[:pass]]@host.domain[:port]/path


  force (optional, bool, False)
    If ``yes`` do not get a cached copy.

    Alias ``thirsty`` has been deprecated and will be removed in 2.13.


  http_agent (optional, str, ansible-httpget)
    Header to identify as, generally appears in web server logs.


  use_proxy (optional, bool, True)
    If ``no``, it will not use a proxy, even if one is defined in an environment variable on the target hosts.


  validate_certs (optional, bool, True)
    If ``no``, SSL certificates will not be validated.

    This should only be used on personally controlled sites using self-signed certificates.


  url_username (optional, str, None)
    The username for use in HTTP basic authentication.

    This parameter can be used without *url_password* for sites that allow empty passwords


  url_password (optional, str, None)
    The password for use in HTTP basic authentication.

    If the *url_username* parameter is not specified, the *url_password* parameter will not be used.


  force_basic_auth (optional, bool, False)
    Credentials specified with *url_username* and *url_password* should be passed in HTTP Header.


  client_cert (optional, path, None)
    PEM formatted certificate chain file to be used for SSL client authentication.

    This file can also include the key as well, and if the key is included, ``client_key`` is not required.


  client_key (optional, path, None)
    PEM formatted file that contains your private key to be used for SSL client authentication.

    If ``client_cert`` contains both the certificate and key, this option is not required.


  use_gssapi (optional, bool, False)
    Use GSSAPI to perform the authentication, typically this is for Kerberos or Kerberos through Negotiate authentication.

    Requires the Python library `gssapi <https://github.com/pythongssapi/python-gssapi>`_ to be installed.

    Credentials for GSSAPI can be specified with *url_username*/*url_password* or with the GSSAPI env var ``KRB5CCNAME`` that specified a custom Kerberos credential cache.

    NTLM authentication is ``not`` supported even if the GSSAPI mech for NTLM has been installed.





Notes
-----

.. note::
   - This module supports check mode.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create an endpoint in icinga
      t_systems_mms.icinga_director.icinga_endpoint:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "fooendpoint"
        host: "127.0.0.1"
        zone: "foozone"

    - name: Update an endpoint in icinga
      t_systems_mms.icinga_director.icinga_endpoint:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "fooendpoint"
        host: "127.0.0.1"
        zone: "foozone"
        port: 5665
        append: true





Status
------





Authors
~~~~~~~

- Aaron Bulmahn (@arbu)

