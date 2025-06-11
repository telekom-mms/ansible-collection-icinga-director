.. _icinga_host_template_module:


icinga_host_template -- Manage host templates in Icinga2
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a host template to Icinga2 through the director API.






Parameters
----------

  accept_config (optional, bool, None)
    Whether the agent is configured to accept config.


  address (optional, str, None)
    Host address. Usually an IPv4 address, but may be any kind of address your check plugin is able to deal with.


  address6 (optional, str, None)
    Host IPv6 address. Usually an IPv6 address, but may be any kind of address your check plugin is able to deal with.


  append (optional, bool, None)
    Do not overwrite the whole object but instead append the defined properties.

    Note - Appending to existing vars, imports or any other list/dict is not possible. You have to overwrite the complete list/dict.

    Note - Variables that are set by default will also be applied, even if not set.


  check_command (optional, str, None)
    The name of the check command.

    Though this is not required to be defined in the director, you still have to supply a check\_command in a host or host-template.


  check_interval (optional, str, None)
    Your regular check interval.


  check_period (optional, str, None)
    The name of a time period which determines when this object should be monitored. Not limited by default.


  check_timeout (optional, str, None)
    Check command timeout in seconds. Overrides the CheckCommand's timeout attribute


  command_endpoint (optional, str, None)
    The endpoint where commands are executed on.


  disabled (optional, bool, False)
    Disabled objects will not be deployed.


  display_name (optional, str, None)
    Alternative name for this host. Might be a host alias or and kind of string helping your users to identify this host.


  enable_active_checks (optional, bool, None)
    Whether to actively check this object.


  enable_event_handler (optional, bool, None)
    Whether to enable event handlers this object.


  enable_flapping (optional, bool, None)
    Whether flap detection is enabled on this object.


  enable_notifications (optional, bool, None)
    Whether to send notifications for this object.


  enable_passive_checks (optional, bool, None)
    Whether to accept passive check results for this object.


  enable_perfdata (optional, bool, None)
    Whether to process performance data provided by this object.


  event_command (optional, str, None)
    Event command for host which gets called on every check execution if one of these conditions matches

    The host is in a soft state

    The host state changes into a hard state

    The host state recovers from a soft or hard state to OK/Up


  flapping_threshold_high (optional, str, None)
    Flapping upper bound in percent for a service to be considered flapping


  flapping_threshold_low (optional, str, None)
    Flapping lower bound in percent for a service to be considered not flapping


  groups (optional, list, [])
    Hostgroups that should be directly assigned to this node. Hostgroups can be useful for various reasons.

    You might assign service checks based on assigned hostgroup. They are also often used as an instrument to enforce restricted views in Icinga Web 2.

    Hostgroups can be directly assigned to single hosts or to host templates.

    You might also want to consider assigning hostgroups using apply rules.


  has_agent (optional, bool, None)
    Whether this host has the Icinga 2 Agent installed.


  icon_image (optional, str, None)
    An URL pointing to an icon for this object.

    Try "tux.png" for icons relative to public/img/icons or "cloud" (no extension) for items from the Icinga icon font


  icon_image_alt (optional, str, None)
    Alternative text to be shown in case above icon is missing


  imports (optional, list, None)
    Choose a host-template.


  master_should_connect (optional, bool, None)
    Whether the parent (master) node should actively try to connect to this agent.


  max_check_attempts (optional, str, None)
    Defines after how many check attempts a new hard state is reached.


  notes (optional, str, None)
    Additional notes for this object.


  notes_url (optional, str, None)
    An URL pointing to additional notes for this object.

    Separate multiple urls like this "'http://url1' 'http://url2'".

    Maximum length is 255 characters.


  object_name (True, str, None)
    Icinga object name for this host template.

    This is usually a fully qualified host name but it could basically be any kind of string.

    To make things easier for your users we strongly suggest to use meaningful names for templates.

    For example "generic-host" is ugly, "Standard Linux Server" is easier to understand.


  retry_interval (optional, str, None)
    Retry interval, will be applied after a state change unless the next hard state is reached.


  state (optional, str, present)
    Apply feature state.


  vars (optional, dict, None)
    Custom properties of the host.


  volatile (optional, bool, None)
    Whether this check is volatile.


  zone (optional, str, None)
    Set the zone.


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

    
    - name: Create host template
      telekom_mms.icinga_director.icinga_host_template:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        accept_config: true
        check_command: hostalive
        check_interval: 90s
        check_timeout: 60
        command_endpoint: fooendpoint
        disabled: false
        display_name: foohosttemplate
        enable_active_checks: true
        enable_event_handler: false
        enable_flapping: false
        enable_notifications: true
        enable_passive_checks: false
        enable_perfdata: false
        flapping_threshold_high: "30.0"
        flapping_threshold_low: "25.0"
        has_agent: true
        icon_image_alt: "alt text"
        icon_image: "http://url1"
        master_should_connect: true
        max_check_attempts: 3
        object_name: foohosttemplate
        retry_interval: "1m"
        volatile: false
        groups:
          - "foohostgroup"
        imports:
          - ''
        vars:
          dnscheck: "no"

    - name: Update host template
      telekom_mms.icinga_director.icinga_host_template:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: foohosttemplate
        notes: "example note"
        notes_url: "'http://url1' 'http://url2'"
        append: true





Status
------





Authors
~~~~~~~

- Michaela Mattes (@michaelamattes)

