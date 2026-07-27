.. _icinga_syncrule_module:


icinga_syncrule -- Manage sync rules in Icinga2 Director
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a sync rule in Icinga2 Director through the director API.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  rule_name (True, str, None)
    Name of the sync rule.

    This must be unique across all sync rules in Icinga Director.


  object_type (False, str, None)
    The Icinga object type that this sync rule targets.

    This is the type of Icinga object that will be created or updated by the sync rule, not to be confused with the Director object\_type (object/template/apply).


  update_policy (False, str, None)
    Defines how existing Icinga objects are updated when the sync rule runs.

    :literal:`merge` merges properties from the import source with existing object properties.

    :literal:`override` replaces all properties of existing objects with values from the import source.

    :literal:`ignore` does not modify existing objects, only creates new ones.

    :literal:`update\-only` only updates existing objects, never creates new ones.


  purge_existing (False, bool, None)
    Whether to remove Icinga objects that are no longer present in the import source.


  purge_action (False, str, None)
    Action to take when purging objects that no longer exist in the import source.

    Only relevant when :literal:`purge\_existing` is :literal:`true`.


  filter_expression (False, str, None)
    An optional filter expression to restrict which imported rows are processed by this sync rule.


  description (False, str, None)
    An optional description for this sync rule.


  sync_properties (False, list, None)
    List of sync property mappings from import\-source columns to Icinga object fields.

    Each entry must contain :literal:`source` (import source name), :literal:`destination\_field` (Icinga property such as :literal:`object\_name`\ , :literal:`address`\ , :literal:`display\_name`\ ), and :literal:`source\_expression` (the column name from the import source).

    Optional per\-entry keys are :literal:`merge\_policy` (default :literal:`override`\ ) and :literal:`filter\_expression`.

    When omitted the module does not manage sync properties (existing properties are preserved).


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
   - Uses the standard :literal:`/director/syncrules` bulk endpoint (GET/POST/DELETE). Requires Director with upstream PR adding POST and DELETE support to :literal:`SyncrulesController` and :literal:`unserializeSyncRules` in :literal:`ImportExport`.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a sync rule in icinga
      telekom_mms.icinga_director.icinga_syncrule:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        rule_name: "Sync Hosts from CMDB"
        object_type: "host"
        update_policy: "merge"
        purge_existing: false
        description: "Synchronizes hosts from the CMDB import source"

    - name: Create a sync rule that purges deleted objects
      telekom_mms.icinga_director.icinga_syncrule:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        rule_name: "Sync Services from CMDB"
        object_type: "service"
        update_policy: "override"
        purge_existing: true
        purge_action: "disable"
        filter_expression: 'source.vars.monitored="yes"'

    - name: Update the description of a sync rule
      telekom_mms.icinga_director.icinga_syncrule:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        rule_name: "Sync Hosts from CMDB"
        description: "Updated description"
        append: true

    - name: Delete a sync rule in icinga
      telekom_mms.icinga_director.icinga_syncrule:
        state: absent
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        rule_name: "Sync Hosts from CMDB"





Status
------





Authors
~~~~~~~

- Michaela Mattes (@mikaEz)

