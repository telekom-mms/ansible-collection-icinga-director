.. _icinga_command_template_module:


icinga_command_template -- Manage command templates in Icinga2
==============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a command template to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  command (optional, str, None)
    The command Icinga should run.

    Absolute paths are accepted as provided, relative paths are prefixed with "PluginDir + ", similar Constant prefixes are allowed.

    Spaces will lead to separation of command path and standalone arguments.

    Please note that this means that we do not support spaces in plugin names and paths right now.


  methods_execute (optional, str, PluginCheck)
    Plugin Check commands are what you need when running checks against your infrastructure.

    Notification commands will be used when it comes to notify your users.

    Event commands allow you to trigger specific actions when problems occur.

    Some people use them for auto-healing mechanisms, like restarting services or rebooting systems at specific thresholds.


  disabled (optional, bool, False)
    Disabled objects will not be deployed.


  object_name (True, str, None)
    Name of the command template.


  imports (optional, list, None)
    Importable templates, add as many as you want. Please note that order matters when importing properties from multiple templates - last one wins.


  timeout (optional, str, None)
    Optional command timeout. Allowed values are seconds or durations postfixed with a specific unit (for example 1m or also 3m 30s).


  zone (optional, str, None)
    Icinga cluster zone. Allows to manually override Directors decisions of where to deploy your config to.

    You should consider not doing so unless you gained deep understanding of how an Icinga Cluster stack works.


  vars (optional, dict, None)
    Custom properties of the command template.


  arguments (optional, dict, None)
    Arguments of the command template.

    Each argument can take either a string, a json or a dict

    When using a dict as argument value, the following properties are supported. ``skip_key``, ``repeat_key``, ``required``, ``order``, ``description``), ``set_if``, ``value``.

    The ``value`` property can be either a string, a json or a dict. When used as a dict, you can define its ``type`` as ``Function`` and set its ``body`` property as an Icinga DSL piece of config.


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

    
    - name: Create command template
      t_systems_mms.icinga_director.icinga_command_template:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        arguments:
          '--authpassphrase':
            value: $snmpv3_priv_key$
          '--authprotocol':
            value: $snmpv3_auth_protocol$
          '--critical':
            value: $centreon_critical$
          '--filter':
            value: $centreon_filter$
          '--hostname':
            value: $snmp_address$
          '--maxrepetitions':
            value: $centreon_maxrepetitions$
          '--mode':
            value: $centreon_mode$
          '--plugin':
            value: $centreon_plugin$
          '--privpassphrase':
            value: $snmpv3_auth_key$
          '--privprotocol':
            value: $snmpv3_priv_protocol$
          '--snmp-community':
            value: $snmp_community$
          '--snmp-timeout':
            value: $snmp_timeout$
          '--snmp-username':
            value: $snmpv3_user$
          '--snmp-version':
            value: $snmp_version$
          '--subsetleef':
            value: $centreon_subsetleef$
          '--verbose':
            set_if: $centreon_verbose$
          '--warning':
            value: $centreon_warning$
          '--dummy-arg':
            description: "dummy arg using Icinga DSL code"
            value:
              type: "Function"
              body: 'return macro("$dummy_var$")'
        command: "/opt/centreon-plugins/centreon_plugins.pl"
        command_type: "PluginCheck"
        object_name: centreon-plugins-template
        disabled: false
        vars:
          centreon_maxrepetitions: 20
          centreon_subsetleef: 20
          centreon_verbose: false
          snmp_address: $address$
          snmp_timeout: 60
          snmp_version: '2'
          snmpv3_auth_key: authkey
          snmpv3_priv_key: privkey
          snmpv3_user: user

    - name: Update command template
      t_systems_mms.icinga_director.icinga_command_template:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: centreon-plugins-template
        timeout: "2m"
        append: true





Status
------





Authors
~~~~~~~

- Lars Krahl (@mmslkr)

