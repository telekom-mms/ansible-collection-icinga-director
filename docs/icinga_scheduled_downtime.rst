.. _icinga_scheduled_downtime_module:


icinga_scheduled_downtime -- Manage downtimes in Icinga2
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a downtime to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  object_name (True, str, None)
    Icinga object name for this downtime.


  disabled (optional, bool, False)
    Disabled objects will not be deployed.


  author (optional, str, None)
    Name of the downtime author.

    Required if *state* is ``present``.


  comment (optional, str, None)
    A descriptive comment for the downtime.

    Required if *state* is ``present``.


  fixed (optional, bool, False)
    Whether this downtime is fixed or flexible. If unsure please check the related documentation https://icinga.com/docs/icinga2/latest/doc/08-advanced-topics/#downtimes

    Required if *state* is ``present``.


  with_services (optional, bool, True)
    Whether you only downtime the hosts or add some services with it.


  ranges (optional, dict, None)
    The period which should be downtimed


  apply_to (optional, str, None)
    Whether this dependency should affect hosts or services

    Required if *state* is ``present``.


  assign_filter (optional, str, None)
    The filter where the downtime will take effect.


  duration (optional, str, None)
    How long the downtime lasts. Only has an effect for flexible (non-fixed) downtimes. Time in seconds, supported suffixes include ms (milliseconds), s (seconds), m (minutes), h (hours) and d (days). To express "90 minutes" you might want to write 1h 30m


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

    
    - name: create icinga_scheduled_downtime
      t_systems_mms.icinga_director.icinga_scheduled_downtime:
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        disabled: false
        object_name: "foodowntime"
        state: present
        author: testuser
        comment: test
        fixed: true
        with_services: true
        apply_to: host
        assign_filter: 'host.name="foohost"'
        duration: 500
        ranges:
          "tuesday": "00:00-24:00"

    - name: create icinga_scheduled_downtime2
      t_systems_mms.icinga_director.icinga_scheduled_downtime:
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        disabled: false
        object_name: "foodowntime2"
        state: present
        author: testuser
        comment: test
        fixed: false
        with_services: false
        apply_to: host
        assign_filter: 'host.name="foohost"'
        duration: 500
        ranges:
          "tuesday": "00:00-24:00"

    - name: update icinga_scheduled_downtime2
      t_systems_mms.icinga_director.icinga_scheduled_downtime:
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "foodowntime2"
        state: present
        duration: 1000
        append: true
        apply_to: host
        with_services: false





Status
------





Authors
~~~~~~~

- Daniel Uhlmann (@xFuture603)

