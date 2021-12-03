.. _icinga_notification_module:


icinga_notification -- Manage notifications in Icinga2
======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a notification to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  object_name (True, str, None)
    Name of the notification.


  notification_interval (optional, str, None)
    The notification interval (in seconds). This interval is used for active notifications.

    Defaults to 30 minutes. If set to 0, re-notifications are disabled.


  types (optional, list, None)
    The state transition types you want to get notifications for.


  users (optional, list, None)
    Users that should be notified by this notification.


  states (optional, list, None)
    The host or service states you want to get notifications for.


  apply_to (optional, str, None)
    Whether this notification should affect hosts or services.

    Required if *state* is ``present``.


  assign_filter (optional, str, None)
    The filter where the notification will take effect.


  imports (optional, list, None)
    Importable templates, add as many as you want. Required when state is ``present``.

    Please note that order matters when importing properties from multiple templates - last one wins.

    Required if *state* is ``present``.


  disabled (optional, bool, False)
    Disabled objects will not be deployed.


  vars (optional, dict, None)
    Custom properties of the notification.


  period (optional, str, None)
    The name of a time period which determines when this notification should be triggered.


  times_begin (optional, int, None)
    First notification delay.

    Delay unless the first notification should be sent.


  times_end (optional, int, None)
    Last notification.

    When the last notification should be sent.


  user_groups (optional, list, None)
    User Groups that should be notified by this notification.


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

    
    - name: Create notification
      t_systems_mms.icinga_director.icinga_notification:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        apply_to: host
        assign_filter: 'host.name="foohost"'
        imports:
          - foonotificationtemplate
        notification_interval: '0'
        object_name: E-Mail_host
        states:
          - Up
          - Down
        types:
          - Problem
          - Recovery
        users:
          - rb
        user_groups:
          - OnCall
        disabled: false
        time_period: "24/7"
        times_begin: 20
        times_end: 120

    - name: Update notification
      t_systems_mms.icinga_director.icinga_notification:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: E-Mail_host
        vars:
          foo: bar
        append: true





Status
------





Authors
~~~~~~~

- Sebastian Gumprich (@rndmh3ro) / Sebastian Gruber (sgruber94)

