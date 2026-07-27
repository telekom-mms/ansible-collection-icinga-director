.. _icinga_importsource_module:


icinga_importsource -- Manage import sources in Icinga2 Director
================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove an import source in Icinga2 Director through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  source_name (True, str, None)
    Name of the import source.

    This must be unique across all import sources in Icinga Director.


  key_column (False, str, None)
    The column name to use as the unique key for imported rows.

    This column must be present in every imported row and must be unique.

    Required when creating a new import source.


  provider_class (False, str, None)
    The fully\-qualified PHP class name of the import source provider.

    Examples are :literal:`Icinga\\Module\\Director\\Import\\RestApiImportSource`\ , :literal:`Icinga\\Module\\Director\\Import\\LdapImportSource` or :literal:`Icinga\\Module\\Director\\Import\\DbImportSource`.

    Required when creating a new import source.


  description (False, str, None)
    An optional description for this import source.


  settings (False, dict, None)
    A dict of provider\-specific settings that are stored as key\-value pairs in the Director import\_source\_setting table.

    The available keys depend on the chosen :literal:`provider\_class`.

    Example for the OTC provider: :literal:`iam\_url`\ , :literal:`username`\ , :literal:`password`\ , :literal:`domain`\ , :literal:`project`\ , :literal:`service\_type`\ , :literal:`resource\_path`.


  modifiers (False, list, None)
    A list of row modifier objects to apply to imported rows.

    Each modifier is a dict with keys :literal:`property\_name`\ , :literal:`target\_property`\ , :literal:`provider\_class` and :literal:`settings`.

    For a regex modifier that extracts an IP address, set :literal:`provider\_class` to :literal:`Icinga\\Module\\Director\\PropertyModifier\\PropertyModifierRegexReplace`.


  append (optional, bool, None)
    Do not overwrite the whole object but instead append the defined properties.

    Note \- Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.

    Note \- Variables that are set by default will also be applied, even if not set.


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

    This should only be used on personally controlled sites using self\-signed certificates.


  url_username (optional, str, None)
    The username for use in HTTP basic authentication.

    This parameter can be used without :literal:`url\_password` for sites that allow empty passwords.


  url_password (optional, str, None)
    The password for use in HTTP basic authentication.

    If the :literal:`url\_username` parameter is not specified, the :literal:`url\_password` parameter will not be used.


  force_basic_auth (optional, bool, False)
    Credentials specified with :literal:`url\_username` and :literal:`url\_password` should be passed in HTTP Header.


  client_cert (optional, path, None)
    PEM formatted certificate chain file to be used for SSL client authentication.

    This file can also include the key as well, and if the key is included, :literal:`client\_key` is not required.


  client_key (optional, path, None)
    PEM formatted file that contains your private key to be used for SSL client authentication.

    If :literal:`client\_cert` contains both the certificate and key, this option is not required.


  use_gssapi (optional, bool, False)
    Use GSSAPI to perform the authentication, typically this is for Kerberos or Kerberos through Negotiate authentication.

    Requires the Python library \ `gssapi <https://github.com/pythongssapi/python-gssapi>`__ to be installed.

    Credentials for GSSAPI can be specified with :literal:`url\_username`\ /\ :literal:`url\_password` or with the GSSAPI env var :envvar:`KRB5CCNAME` that specified a custom Kerberos credential cache.

    NTLM authentication is :strong:`not` supported even if the GSSAPI mech for NTLM has been installed.


  api_timeout (optional, int, 10)
    Default timeout to wait for transaction to finish in seconds.





Notes
-----

.. note::
   - This module supports check mode.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create an import source in icinga
      telekom_mms.icinga_director.icinga_importsource:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        source_name: "My Import Source"
        key_column: "hostname"
        provider_class: "Icinga\\Module\\Director\\Import\\RestApiImportSource"
        description: "Import hosts from REST API"

    - name: Update the description of an import source
      telekom_mms.icinga_director.icinga_importsource:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        source_name: "My Import Source"
        description: "Updated description"
        append: true

    - name: Delete an import source in icinga
      telekom_mms.icinga_director.icinga_importsource:
        state: absent
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        source_name: "My Import Source"





Status
------





Authors
~~~~~~~

- Michaela Mattes (@mikaEz)

