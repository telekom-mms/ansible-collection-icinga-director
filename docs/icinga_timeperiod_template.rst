.. _icinga_timeperiod_template_module:


icinga_timeperiod_template -- Manage timeperiod templates in Icinga2
====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a timeperiod template to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  object_name (True, str, None)
    Name of the time period.


  display_name (optional, str, None)
    Alternative name for this timeperiod template.


  disabled (optional, bool, False)
    Disabled objects will not be deployed.


  imports (optional, list, None)
    Importable templates, add as many as you want.

    Please note that order matters when importing properties from multiple templates - last one wins.


  includes (optional, list, None)
    Include other time periods into this.


  excludes (optional, list, None)
    Exclude other time periods from this.


  prefer_includes (optional, bool, True)
    Whether to prefer timeperiods includes or excludes. Default to true.


  ranges (optional, dict, None)
    A dict of days and timeperiods.


  zone (optional, str, None)
    Set the zone.


  update_method (optional, str, LegacyTimePeriod)
    Define the update method.


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

    
    - name: Create timeperiod template
      t_systems_mms.icinga_director.icinga_timeperiod_template:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "timeperiod_template"
        imports: []
        disabled: false
        prefer_includes: false
        ranges:
          monday: "00:00-23:59"
          tuesday: "00:00-23:59"
          wednesday: "00:00-23:59"
          thursday: "00:00-23:59"
          friday: "00:00-23:59"
          saturday: "00:00-23:59"
          sunday: "00:00-23:59"
        update_method: "LegacyTimePeriod"

    - name: Update timeperiod template
      t_systems_mms.icinga_director.icinga_timeperiod_template:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "timeperiod_template"
        display_name: "timeperiod template"
        append: true





Status
------





Authors
~~~~~~~

- Sebastian Gumprich (@rndmh3ro)

