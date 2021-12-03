.. _icinga_host_template_module:


icinga_host_template -- Manage host templates in Icinga2
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a host template to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  object_name (True, str, None)
    Icinga object name for this host template.

    This is usually a fully qualified host name but it could basically be any kind of string.

    To make things easier for your users we strongly suggest to use meaningful names for templates.

    For example "generic-host" is ugly, "Standard Linux Server" is easier to understand.


  display_name (optional, str, None)
    Alternative name for this host.

    Might be a host alias or and kind of string helping your users to identify this host.


  address (optional, str, None)
    Host address. Usually an IPv4 address, but may be any kind of address your check plugin is able to deal with.


  address6 (optional, str, None)
    Host IPv6 address. Usually an IPv64 address, but may be any kind of address your check plugin is able to deal with.


  groups (optional, list, [])
    Hostgroups that should be directly assigned to this node. Hostgroups can be useful for various reasons.

    You might assign service checks based on assigned hostgroup. They are also often used as an instrument to enforce restricted views in Icinga Web 2.

    Hostgroups can be directly assigned to single hosts or to host templates.

    You might also want to consider assigning hostgroups using apply rules.


  check_command (optional, str, None)
    The name of the check command.

    Though this is not required to be defined in the director, you still have to supply a check_command in a host or host-template.


  event_command (optional, str, None)
    Event command for host which gets called on every check execution if one of these conditions matches

    The host is in a soft state

    The host state changes into a hard state

    The host state recovers from a soft or hard state to OK/Up


  check_interval (optional, str, None)
    Your regular check interval.


  retry_interval (optional, str, None)
    Retry interval, will be applied after a state change unless the next hard state is reached.


  disabled (optional, bool, False)
    Disabled objects will not be deployed.


  imports (optional, list, None)
    Choose a host-template.


  max_check_attempts (optional, str, None)
    Defines after how many check attempts a new hard state is reached.


  zone (optional, str, None)
    Set the zone.


  vars (optional, dict, None)
    Custom properties of the host.


  notes (optional, str, None)
    Additional notes for this object.


  notes_url (optional, str, None)
    An URL pointing to additional notes for this object.

    Separate multiple urls like this "'http://url1' 'http://url2'".

    Maximum length is 255 characters.


  has_agent (optional, bool, None)
    Whether this host has the Icinga 2 Agent installed.


  master_should_connect (optional, bool, None)
    Whether the parent (master) node should actively try to connect to this agent.


  accept_config (optional, bool, None)
    Whether the agent is configured to accept config.


  command_endpoint (optional, str, None)
    The endpoint where commands are executed on.


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

    
    - name: Create host template
      t_systems_mms.icinga_director.icinga_host_template:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: foohosttemplate
        display_name: foohosttemplate
        disabled: false
        check_command: dummy
        check_interval: 90s
        retry_interval: 30s
        groups:
          - "foohostgroup"
        imports:
          - ''
        has_agent: true
        master_should_connect: true
        max_check_attempts: 3
        accept_config: true
        command_endpoint: fooendpoint

    - name: Update host template
      t_systems_mms.icinga_director.icinga_host_template:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: foohosttemplate
        notes: "example note"
        notes_url: "'http://url1' 'http://url2'"
        append: true





Status
------





Authors
~~~~~~~

- Michaela Mattes (@michaelamattes)

