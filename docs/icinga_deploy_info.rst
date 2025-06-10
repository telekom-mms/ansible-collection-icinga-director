.. _icinga_deploy_info_module:


icinga_deploy_info -- Get deployment information through the director API
=========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get deployment information through the director API.






Parameters
----------

  configs (optional, list, None)
    A list of checksums of configs to query information for


  activities (optional, list, None)
    A list of checksums of activities to query information for


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









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Query the current deployment info in icinga
      telekom_mms.icinga_director.icinga_deploy_info:
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"



Return Values
-------------

active_configuration (if active configuration exists, dict, {'active_configuration': {'activity': '3557598829f2a2fc4acc7b565fb54bae24754c67', 'config': '299d9d49e03435c6de562c4b22a26e63990d30a9', 'stage_name': '902cb282-e702-43ce-bb3c-962f850a1694'}})
  Checksums of the active configuration

  Contains current activity checksum, config checksum

  and a checksum for the stage\_name


configs (only if requested, list, {'configs': {'b175ca0562434deeb4fb1fc03fd80cd7361b56df': 'deployed', 'b175ca0562434deeb4fb1fc03fd80cd7361b56de': 'active'}})
  Checksum of the requested config and its state


activities (only if requested, list, {'activities': {'a4c955364bc7b77efd0323fc87d95307f827e30c': 'deployed', '3557598829f2a2fc4acc7b565fb54bae24754c67': 'active'}})
  checksum of the requested activities and its state





Status
------





Authors
~~~~~~~

- Falk Händler (@flkhndlr)

