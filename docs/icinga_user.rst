.. _icinga_user_module:


icinga_user -- Manage users in Icinga2
======================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a user to Icinga2 through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  object_name (True, str, None)
    Name of the user.


  display_name (optional, str, None)
    Alternative name for this user.

    In case your object name is a username, this could be the full name of the corresponding person.


  imports (optional, list, None)
    Importable templates, add as many as you want.

    Please note that order matters when importing properties from multiple templates - last one wins.


  pager (optional, str, None)
    The pager address of the user.


  period (optional, str, None)
    The name of a time period which determines when notifications to this User should be triggered. Not set by default.


  disabled (optional, bool, False)
    Disabled objects will not be deployed.


  email (optional, str, None)
    The Email address of the user.


  groups (optional, list, None)
    User groups that should be directly assigned to this user.

    Groups can be useful for various reasons. You might prefer to send notifications to groups instead of single users.


  vars (optional, dict, {})
    Custom properties of the user.


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

    
    - name: Create user
      telekom_mms.icinga_director.icinga_user:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "rb"
        pager: 'SIP/emergency'
        period: '24/7'
        email: "foouser@example.com"
        imports:
          - foousertemplate
        groups:
          - onCall
        vars:
          department: IT
          role: CTO

    - name: Update user
      telekom_mms.icinga_director.icinga_user:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "rb"
        display_name: "Rufbereitschaft"
        append: true





Status
------





Authors
~~~~~~~

- Sebastian Gumprich (@rndmh3ro)

