.. _icinga_job_module:


icinga_job -- Manage director jobs in Icinga2 Director
======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Add or remove a director job in Icinga2 Director through the director API.

Director jobs allow scheduling automatic import and sync runs as well as other recurring tasks.






Parameters
----------

  state (optional, str, present)
    Apply feature state.


  job_name (True, str, None)
    Name of the director job.

    This must be unique across all jobs in Icinga Director.


  job_class (False, str, None)
    The fully\-qualified PHP class name of the job implementation.

    Examples are :literal:`Icinga\\Module\\Director\\Job\\ImportRunJob` to run an import source or :literal:`Icinga\\Module\\Director\\Job\\SyncRunJob` to run a sync rule.

    Required when creating a new job.


  disabled (False, bool, False)
    Whether this job is disabled and should not be run automatically.


  run_interval (False, int, None)
    How often the job should run, in seconds.

    Required when creating a new job.


  timeperiod (False, str, None)
    The name of a time period which restricts when this job may run.

    If not set the job may run at any time.


  settings (False, dict, None)
    A dict of job\-class\-specific settings stored as key\-value pairs in the Director director\_job\_setting table.

    For :literal:`Icinga\\Module\\Director\\Job\\ImportJob` use :literal:`source\_name` to reference the import source by name and :literal:`run\_import` set to :literal:`"y"` to actually run the import (default :literal:`"n"` only checks for changes).

    For :literal:`Icinga\\Module\\Director\\Job\\SyncJob` use :literal:`rule\_name` to reference the sync rule by name and :literal:`apply\_changes` set to :literal:`"y"` to actually apply changes (default :literal:`"n"` only checks).


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
   - Uses the standard :literal:`/director/jobs` bulk endpoint (GET/POST/DELETE). Requires Director with upstream PR adding POST and DELETE support to :literal:`JobsController` and :literal:`unserializeJobs` in :literal:`ImportExport`.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a director job to run an import source
      telekom_mms.icinga_director.icinga_job:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        job_name: "Run CMDB Import"
        job_class: "Icinga\\Module\\Director\\Job\\ImportRunJob"
        run_interval: 3600
        disabled: false

    - name: Create a director job to run a sync rule during business hours
      telekom_mms.icinga_director.icinga_job:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        job_name: "Run Host Sync"
        job_class: "Icinga\\Module\\Director\\Job\\SyncRunJob"
        run_interval: 900
        timeperiod: "business-hours"

    - name: Disable a director job
      telekom_mms.icinga_director.icinga_job:
        state: present
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        job_name: "Run CMDB Import"
        disabled: true
        append: true

    - name: Delete a director job
      telekom_mms.icinga_director.icinga_job:
        state: absent
        url: "{{ icinga_url }}"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        job_name: "Run CMDB Import"





Status
------





Authors
~~~~~~~

- Michaela Mattes (@mikaEz)

