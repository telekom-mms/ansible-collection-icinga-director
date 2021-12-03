.. _icinga_service_apply_module:


icinga_service_apply -- Manage service apply rules in Icinga2
=============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a service apply rule to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  object_name (True, str, None)
    Name for the Icinga service apply rule.


  display_name (optional, str, None)
    Alternative displayed name of the service apply rule.


  check_command (optional, str, None)
    Check command definition.


  check_interval (False, str, None)
    Your regular check interval.


  check_period (False, str, None)
    The name of a time period which determines when this object should be monitored. Not limited by default.


  check_timeout (False, str, None)
    Check command timeout in seconds. Overrides the CheckCommand's timeout attribute.


  enable_active_checks (False, bool, None)
    Whether to actively check this object.


  enable_event_handler (False, bool, None)
    Whether to enable event handlers this object.


  enable_notifications (False, bool, None)
    Whether to send notifications for this object.


  enable_passive_checks (False, bool, None)
    Whether to accept passive check results for this object.


  enable_perfdata (False, bool, None)
    Whether to process performance data provided by this object.


  event_command (False, str, None)
    Event command for service which gets called on every check execution if one of these conditions matches

    The service is in a soft state

    The service state changes into a hard state

    The service state recovers from a soft or hard state to OK/Up


  max_check_attempts (False, str, None)
    Defines after how many check attempts a new hard state is reached.


  retry_interval (False, str, None)
    Retry interval, will be applied after a state change unless the next hard state is reached.


  groups (optional, list, None)
    Service groups that should be directly assigned to this service.

    Servicegroups can be useful for various reasons.

    They are helpful to provided service-type specific view in Icinga Web 2, either for custom dashboards or as an instrument to enforce restrictions.

    Service groups can be directly assigned to single services or to service templates.


  apply_for (optional, str, None)
    Evaluates the apply for rule for all objects with the custom attribute specified.

    For example selecting "host.vars.custom_attr" will generate "for (config in host.vars.array_var)" where "config" will be accessible through "$config$".

    Note - only custom variables of type "Array" are eligible.


  assign_filter (optional, str, None)
    The filter where the service apply rule will take effect.


  command_endpoint (optional, str, None)
    The host where the service should be executed on.


  imports (optional, list, None)
    Importable templates, add as many as you want.

    Please note that order matters when importing properties from multiple templates - last one wins.


  vars (optional, dict, None)
    Custom properties of the service apply rule.


  notes (optional, str, None)
    Additional notes for this object.


  notes_url (optional, str, None)
    An URL pointing to additional notes for this object.

    Separate multiple urls like this "'http://url1' 'http://url2'".

    Maximum length is 255 characters.


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

    
    - name: Add service apply rule to icinga
      t_systems_mms.icinga_director.icinga_service_apply:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "SERVICE_dummy"
        assign_filter: 'host.name="foohost"'
        check_command: hostalive
        display_name: "dummy process"
        check_interval: "10m"
        check_period: "24/7"
        check_timeout: "1m"
        enable_active_checks: true
        enable_event_handler: true
        enable_notifications: true
        enable_passive_checks: false
        enable_perfdata: false
        event_command: restart_httpd
        max_check_attempts: "5"
        retry_interval: "3m"
        imports:
          - fooservicetemplate
        groups:
          - fooservicegroup
        vars:
          http_address: "$address$"
          http_port: "9080"
          http_uri: "/ready"
          http_string: "Ready"
          http_expect: "Yes"

    - name: Add service apply rule with command_endpoint
      t_systems_mms.icinga_director.icinga_service_apply:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "SERVICE_dummy"
        assign_filter: 'host.name="foohost"'
        check_command: hostalive
        display_name: "dummy process"
        check_interval: "10m"
        check_period: "24/7"
        check_timeout: "1m"
        enable_active_checks: true
        enable_event_handler: true
        enable_notifications: true
        enable_passive_checks: false
        event_command: restart_httpd
        max_check_attempts: "5"
        retry_interval: "3m"
        command_endpoint: "fooendpoint"
        imports:
          - fooservicetemplate
        groups:
          - fooservicegroup

    - name: Update service apply rule with command_endpoint
      t_systems_mms.icinga_director.icinga_service_apply:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "SERVICE_dummy"
        enable_perfdata: true
        append: true





Status
------





Authors
~~~~~~~

- Sebastian Gumprich (@rndmh3ro)

