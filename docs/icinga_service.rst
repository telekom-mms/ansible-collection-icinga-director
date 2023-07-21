.. _icinga_service_module:


icinga_service -- Manage services in Icinga2
============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a service to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  object_name (True, str, None)
    Name of the service.


  check_command (optional, str, None)
    Check command definition.


  check_interval (optional, str, None)
    Your regular check interval.


  check_period (optional, str, None)
    The name of a time period which determines when this object should be monitored. Not limited by default.


  check_timeout (optional, str, None)
    Check command timeout in seconds. Overrides the CheckCommand's timeout attribute.


  display_name (optional, str, None)
    Alternative name for this service.


  enable_active_checks (optional, bool, None)
    Whether to actively check this object.


  enable_event_handler (optional, bool, None)
    Whether to enable event handlers this object.


  enable_notifications (optional, bool, None)
    Whether to send notifications for this object.


  enable_passive_checks (optional, bool, None)
    Whether to accept passive check results for this object.


  enable_perfdata (optional, bool, None)
    Whether to process performance data provided by this object.


  groups (optional, list, [])
    Service groups that should be directly assigned to this service.

    Servicegroups can be useful for various reasons.

    They are helpful to provided service-type specific view in Icinga Web 2, either for custom dashboards or as an instrument to enforce restrictions.

    Service groups can be directly assigned to single services or to service templates.


  host (False, str, None)
    Choose the host this single service should be assigned to.

    This field will be required when \`service\_set\` is not defined.


  imports (optional, list, [])
    Importable templates, add as many as you want.

    Please note that order matters when importing properties from multiple templates - last one wins.


  max_check_attempts (optional, str, None)
    Defines after how many check attempts a new hard state is reached.


  notes (optional, str, None)
    Additional notes for this object.


  notes_url (optional, str, None)
    An URL pointing to additional notes for this object.

    Separate multiple urls like this "'http://url1' 'http://url2'".

    Maximum length is 255 characters.


  retry_interval (optional, str, None)
    Retry interval, will be applied after a state change unless the next hard state is reached.


  use_agent (optional, bool, None)
    Whether the check command for this service should be executed on the Icinga agent.


  vars (optional, dict, {})
    Custom properties of the service.


  volatile (optional, bool, None)
    Whether this check is volatile.


  disabled (optional, bool, False)
    Disabled objects will not be deployed.


  append (optional, bool, None)
    Do not overwrite the whole object but instead append the defined properties.

    Note - Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.

    Note - Variables that are set by default will also be applied, even if not set.


  service_set (optional, str, None)
    Choose the service set name this single service should be assigned to.

    This field will be required when \`host\` is not defined.


  url (True, str, None)
    HTTP, HTTPS, or FTP URL in the form (http|https|ftp)://[user[:pass]]@host.domain[:port]/path


  force (optional, bool, False)
    If \ :literal:`yes`\  do not get a cached copy.


  http_agent (optional, str, ansible-httpget)
    Header to identify as, generally appears in web server logs.


  use_proxy (optional, bool, True)
    If \ :literal:`no`\ , it will not use a proxy, even if one is defined in an environment variable on the target hosts.


  validate_certs (optional, bool, True)
    If \ :literal:`no`\ , SSL certificates will not be validated.

    This should only be used on personally controlled sites using self-signed certificates.


  url_username (optional, str, None)
    The username for use in HTTP basic authentication.

    This parameter can be used without \ :emphasis:`url\_password`\  for sites that allow empty passwords


  url_password (optional, str, None)
    The password for use in HTTP basic authentication.

    If the \ :emphasis:`url\_username`\  parameter is not specified, the \ :emphasis:`url\_password`\  parameter will not be used.


  force_basic_auth (optional, bool, False)
    Credentials specified with \ :emphasis:`url\_username`\  and \ :emphasis:`url\_password`\  should be passed in HTTP Header.


  client_cert (optional, path, None)
    PEM formatted certificate chain file to be used for SSL client authentication.

    This file can also include the key as well, and if the key is included, \ :literal:`client\_key`\  is not required.


  client_key (optional, path, None)
    PEM formatted file that contains your private key to be used for SSL client authentication.

    If \ :literal:`client\_cert`\  contains both the certificate and key, this option is not required.


  use_gssapi (optional, bool, False)
    Use GSSAPI to perform the authentication, typically this is for Kerberos or Kerberos through Negotiate authentication.

    Requires the Python library \ `gssapi <https://github.com/pythongssapi/python-gssapi>`__\  to be installed.

    Credentials for GSSAPI can be specified with \ :emphasis:`url\_username`\ /\ :emphasis:`url\_password`\  or with the GSSAPI env var \ :literal:`KRB5CCNAME`\  that specified a custom Kerberos credential cache.

    NTLM authentication is \ :literal:`not`\  supported even if the GSSAPI mech for NTLM has been installed.





Notes
-----

.. note::
   - This module supports check mode.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create service
      tags: service
      t_systems_mms.icinga_director.icinga_service:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "foo service"
        display_name: "foo service"
        check_command: hostalive
        use_agent: false
        host: foohost
        vars:
          procs_argument: consul
          procs_critical: '1:'
          procs_warning: '1:'

    - name: Update service
      tags: service
      t_systems_mms.icinga_director.icinga_service:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "foo service"
        display_name: "foo service"
        host: foohost
        notes: "example note"
        notes_url: "'http://url1' 'http://url2'"
        append: true

    - name: Create serviceset service
      t_systems_mms.icinga_director.icinga_service:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "foo service serviceset"
        service_set: "foo_serviceset"





Status
------


- This module will be removed in version
  3.0.0.
  *[deprecated]*


Authors
~~~~~~~

- Sebastian Gumprich (@rndmh3ro)

