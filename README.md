Icinga Director Collection for Ansible
=========

[![ci-ansible-test](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/workflows/ansible-test/badge.svg)](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/actions?query=workflow%3Aansible-test)
[![codecov](https://codecov.io/gh/T-Systems-MMS/ansible-collection-icinga-director/branch/master/graph/badge.svg)](https://codecov.io/gh/T-Systems-MMS/ansible-collection-icinga-director)

This collection contains Ansible [modules](plugins/modules/) and a [role](roles/ansible_icinga/) to change objects in Icinga 2 using the director API.

Required Ansible version: 2.9

Currently supported modules:

* `icinga_command_template`
* `icinga_command`
* `icinga_endpoint`
* `icinga_host_template`
* `icinga_host`
* `icinga_hostgroup`
* `icinga_notification`
* `icinga_notification_template`
* `icinga_service`
* `icinga_service_apply`
* `icinga_service_template`
* `icinga_servicegroup`
* `icinga_timeperiod`
* `icinga_user_template`
* `icinga_user`
* `icinga_zone`

Installation
------------

These modules are distributed as [collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).
To install them, run:

```
ansible-galaxy collection install t_systems_mms.icinga_director
```

Alternatively put the collection into a `requirements.yml`-file:

```
---
collections:
- t_systems_mms.icinga_director
```

Examples using the modules
--------------------------

See the `examples` directory for a complete list of examples.

```
- hosts: localhost
  collections:
    - t_systems_mms.icinga_director
  tasks:
    - name: create a host in icinga
      t_systems_mms.icinga_director.icinga_host:
        state: present
        url: "https://example.com"
        url_username: "{{ icinga_user }}"
        url_password: "{{ icinga_pass }}"
        object_name: "{{ ansible_hostname }}"
        address: "{{ ansible_default_ipv4.address }}"
        display_name: "{{ ansible_hostname }}"
        groups:
          - "foo"
        imports:
          - "StandardServer"
        vars:
          dnscheck: "no"
```

Examples using the role
-----------------------

Please see the [README](roles/ansible_icinga/README.md) of the role.

Troubleshooting
---------------

If the following error is thrown, check if you're behind a proxy and use `force_basic_auth: true` in the task.

```
fatal: [localhost]: FAILED! => {"changed": false, "msg": "bad return code while creating: -1. Error message: Request failed: <urlopen error Tunnel connection failed: 302 Found>"}
```

Local Testing
-------------

* Linting with tox

```
> tox -elinters
```

* Integration tests with docker

```
# run icinga in a container and forward port 80
> docker run -d -p 80:80 jordan/icinga2

# run the ansible playbooks against the container
> ansible-playbook tests/integration/targets/icinga/normalmode.yml
> ansible-playbook tests/integration/targets/icinga/checkmode.yml
```

Extras
------

* Use our code snippets template supported in Visual Studio Code

Please see the [README](vsc-snippets/README.md) for more information.


License
-------

GPLv3

Author Information
------------------

* Sebastian Gumprich
* Lars Krahl
* Michaela Mattes
