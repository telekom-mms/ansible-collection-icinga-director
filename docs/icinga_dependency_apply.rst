.. _icinga_dependency_apply_module:


icinga_dependency_apply -- Manage dependency apply rules in Icinga2
===================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a dependency apply rule to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  object_name (True, str, None)
    Name for the Icinga dependency apply rule.


  imports (optional, list, None)
    Importable templates, add as many as you want. Required when state is :literal:`present`.

    Please note that order matters when importing properties from multiple templates - last one wins.

    Required if :emphasis:`state` is :literal:`present`.


  apply_to (optional, str, None)
    Whether this notification should affect hosts or services.

    Required if :emphasis:`state` is :literal:`present`.


  parent_host (optional, str, None)
    The parent host. You can refer to Host Custom Variables via $host.vars.varname$


  parent_service (optional, str, None)
    The parent service. If omitted this dependency object is treated as host dependency. You can refer to Host Custom Variables via $host.vars.varname$


  disable_checks (False, bool, None)
    Whether to disable checks when this dependency fails.


  disable_notifications (False, bool, None)
    Whether to disable notifications when this dependency fails.


  ignore_soft_states (False, bool, None)
    Whether to ignore soft states for the reachability calculation.


  period (False, str, None)
    The name of a time period which determines when this notification should be triggered.


  zone (False, str, None)
    Icinga cluster zone.


  states (False, list, [])
    The host/service states you want to get notifications for.


  append (optional, bool, None)
    Do not overwrite the whole object but instead append the defined properties.

    Note - Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.

    Note - Variables that are set by default will also be applied, even if not set.


  assign_filter (optional, str, None)
    The filter where the service apply rule will take effect.


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

    
    - name: Add dependency apply to icinga
      telekom_mms.icinga_director.icinga_dependency_apply:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: foodependencyapply
        imports:
          - footdependencytemplate
        apply_to: host
        assign_filter: 'host.name="foohost"'

    - name: Add dependency apply to icinga with customization
      telekom_mms.icinga_director.icinga_dependency_apply:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: foodependencyapplycustom
        imports:
          - footdependencytemplate
        apply_to: host
        parent_host: $host.vars.variable$
        assign_filter: 'host.name="foohost"'
        disable_checks: true
        disable_notifications: true
        ignore_soft_states: false
        period: "24/7"
        zone: master
        states:
          - Critical
          - Warning

    - name: Update dependency apply rule with ignore_soft_states
      telekom_mms.icinga_director.icinga_dependency_apply:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: foodependencyapply
        ignore_soft_states: true
        append: true





Status
------





Authors
~~~~~~~

- Gianmarco Mameli (@gianmarco-mameli)

