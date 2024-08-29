.. _icinga_director_inventory_module:


icinga_director_inventory -- Returns Ansible inventory from Icinga
==================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Returns Ansible inventory from Icinga






Parameters
----------

  plugin (True, any, None)
    Name of the plugin


  url (True, str, None)
    Icinga URL to connect to


  url_username (optional, str, None)
    The username for use in HTTP basic authentication.

    This parameter can be used without \`url\_password\` for sites that allow empty passwords


  url_password (optional, str, None)
    The password for use in HTTP basic authentication.

    If the \`url\_username\` parameter is not specified, the \`url\_password\` parameter will not be used.


  force_basic_auth (optional, bool, False)
    Credentials specified with \`url\_username\` and \`url\_password\` should be passed in HTTP Header.


  client_cert (optional, path, None)
    PEM formatted certificate chain file to be used for SSL client authentication.

    This file can also include the key as well, and if the key is included, \`client\_key\` is not required.


  client_key (optional, path, None)
    PEM formatted file that contains your private key to be used for SSL client authentication.

    If \`client\_cert\` contains both the certificate and key, this option is not required.


  http_agent (optional, str, ansible-httpget)
    Header to identify as, generally appears in web server logs.


  use_proxy (optional, bool, True)
    If \`no\`, it will not use a proxy, even if one is defined in an environment variable on the target hosts.


  validate_certs (optional, bool, True)
    If \`no\`, SSL certificates will not be validated.

    This should only be used on personally controlled sites using self-signed certificates.


  use_gssapi (optional, bool, False)
    Use GSSAPI to perform the authentication, typically this is for Kerberos or Kerberos through Negotiate authentication.

    Requires the Python library \`gssapi \<https://github.com/pythongssapi/python-gssapi\>\` to be installed.

    Credentials for GSSAPI can be specified with \`url\_username\`/ \`url\_password\`

    or with the GSSAPI env var \`KRB5CCNAME\` that specified a custom Kerberos credential cache.

    NTLM authentication is \`not\` supported even if the GSSAPI mech for NTLM has been installed.


  force (optional, bool, False)
    If :literal:`yes` do not get a cached copy.


  strict (optional, bool, False)
    If :literal:`yes` make invalid entries a fatal error, otherwise skip and continue.

    Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.


  compose (optional, dict, {})
    Create vars from jinja2 expressions.


  groups (optional, dict, {})
    Add hosts to group based on Jinja2 conditionals.


  keyed_groups (optional, list, [])
    Add hosts to group based on the values of a variable.


    parent_group (optional, str, None)
      parent group for keyed group


    prefix (optional, str, )
      A keyed group name will start with this prefix


    separator (optional, str, _)
      separator used to build the keyed group name


    key (optional, str, None)
      The key from input dictionary used to generate groups


    default_value (optional, str, None)
      The default value when the host variable's value is an empty string.

      This option is mutually exclusive with :literal:`trailing\_separator`.


    trailing_separator (optional, bool, True)
      Set this option to :emphasis:`False` to omit the :literal:`separator` after the host variable when the value is an empty string.

      This option is mutually exclusive with :literal:`default\_value`.



  use_extra_vars (optional, bool, False)
    Merge extra vars into the available variables for composition (highest precedence).


  leading_separator (optional, boolean, True)
    Use in conjunction with keyed\_groups.

    By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore.

    This is because the default prefix is "" and the default separator is "\_".

    Set this option to False to omit the leading underscore (or other separator) if no prefix is given.

    If the group name is derived from a mapping the separator is still used to concatenate the items.

    To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead.









Examples
--------

.. code-block:: yaml+jinja

    
    plugin: telekom_mms.icinga_director.icinga_director_inventory
    url: 'https://example.com'
    url_username: foo
    url_password: bar
    force_basic_auth: False
    strict: False

    # use the object_name you defined as hostname
    compose:
      hostname: object_name

    # create a group based on the operating system defined in a custom variable
    keyed_groups:
      - prefix: os
        key: vars.HostOS

    # create groups based on jinja templates
    # here we create a group called "rb" if the host variable "check_period" is "24/7"
    groups:
      rb: check_period == "24/7"





Status
------





Authors
~~~~~~~

- Sebastian Gumprich (@rndmh3ro)

