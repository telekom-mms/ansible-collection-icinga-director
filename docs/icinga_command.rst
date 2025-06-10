.. _icinga_command_module:


icinga_command -- Manage commands in Icinga2
============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a command to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  command (optional, str, None)
    The command Icinga should run. Required when state is :literal:`present`.

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
    Name of the command.


  imports (optional, list, [])
    Importable templates, add as many as you want. Please note that order matters when importing properties from multiple templates - last one wins.


  timeout (optional, str, None)
    Optional command timeout. Allowed values are seconds or durations postfixed with a specific unit (for example 1m or also 3m 30s).


  zone (optional, str, None)
    Icinga cluster zone. Allows to manually override Directors decisions of where to deploy your config to.

    You should consider not doing so unless you gained deep understanding of how an Icinga Cluster stack works.


  vars (optional, dict, {})
    Custom properties of the command.


  arguments (optional, dict, None)
    Arguments of the command.

    Each argument can take either a string, a json or a dict

    When using a dict as argument value, the following properties are supported. :literal:`skip\_key`\ , :literal:`repeat\_key`\ , :literal:`required`\ , :literal:`order`\ , :literal:`description`\ ), :literal:`set\_if`\ , :literal:`value`.

    The :literal:`value` property can be either a string, a json or a dict. When used as a dict, you can define its :literal:`type` as :literal:`Function` and set its :literal:`body` property as an Icinga DSL piece of config.


  append (optional, bool, None)
    Do not overwrite the whole object but instead append the defined properties.

    Note - Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.

    Note - Variables that are set by default will also be applied, even if not set.


  url (True, str, None)
    HTTP, HTTPS, or FTP URL in the form (http\|https\|ftp)://[user[:pass]]@host.domain[:port]/path


  force (optional, bool, False)
    If :literal:`yes` do not get a cached copy.


  http_agent (optional, str, ansible-httpget)
    Header to identify as, generally appears in web server logs.


  use_proxy (optional, bool, True)
    If :literal:`no`\ , it will not use a proxy, even if one is defined in an environment variable on the target hosts.


  validate_certs (optional, bool, True)
    If :literal:`no`\ , SSL certificates will not be validated.

    This should only be used on personally controlled sites using self-signed certificates.


  url_username (optional, str, None)
    The username for use in HTTP basic authentication.

    This parameter can be used without :emphasis:`url\_password` for sites that allow empty passwords


  url_password (optional, str, None)
    The password for use in HTTP basic authentication.

    If the :emphasis:`url\_username` parameter is not specified, the :emphasis:`url\_password` parameter will not be used.


  force_basic_auth (optional, bool, False)
    Credentials specified with :emphasis:`url\_username` and :emphasis:`url\_password` should be passed in HTTP Header.


  client_cert (optional, path, None)
    PEM formatted certificate chain file to be used for SSL client authentication.

    This file can also include the key as well, and if the key is included, :literal:`client\_key` is not required.


  client_key (optional, path, None)
    PEM formatted file that contains your private key to be used for SSL client authentication.

    If :literal:`client\_cert` contains both the certificate and key, this option is not required.


  use_gssapi (optional, bool, False)
    Use GSSAPI to perform the authentication, typically this is for Kerberos or Kerberos through Negotiate authentication.

    Requires the Python library \ `gssapi <https://github.com/pythongssapi/python-gssapi>`__ to be installed.

    Credentials for GSSAPI can be specified with :emphasis:`url\_username`\ /\ :emphasis:`url\_password` or with the GSSAPI env var :literal:`KRB5CCNAME` that specified a custom Kerberos credential cache.

    NTLM authentication is :literal:`not` supported even if the GSSAPI mech for NTLM has been installed.


  api_timeout (optional, int, 10)
    Default timeout to wait for transaction to finish in seconds.





Notes
-----

.. note::
   - This module supports check mode.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create command
      telekom_mms.icinga_director.icinga_command:
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
        disabled: false
        object_name: centreon-plugins
        imports:
          - centreon-plugins-template
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

    - name: Update command
      telekom_mms.icinga_director.icinga_command:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: centreon-plugins
        timeout: "1m"
        append: true

    - name: Create event command
      telekom_mms.icinga_director.icinga_command:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        command: "/opt/scripts/restart_httpd"
        object_name: "restart_httpd"
        command_type: "PluginEvent"
        arguments:
          '-s':
            value: $service.state$
          '-t':
            value: $service.state_type$
          '-a':
            set_if: $service.check_attempt$
            value: $restart_service$





Status
------





Authors
~~~~~~~

- Sebastian Gumprich (@rndmh3ro)

