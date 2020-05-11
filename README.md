Icinga Director Collection for Ansible
=========

[![ci-ansible-test](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/workflows/ansible-test/badge.svg)](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/actions?query=workflow%3Aansible-test)
[![ci-ansible-lint](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/workflows/Ansible%20Lint/badge.svg)](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/actions?query=workflow%3A%22Ansible+Lint%22)

This collection contains Ansible modules to change objects in Icinga 2 using the director API.

Currently supported modules:

* `icinga_command`
* `icinga_host`
* `icinga_hostgroup`
* `icinga_notification`
* `icinga_service_apply`
* `icinga_service_template`
* `icinga_servicegroup`
* `icinga_timeperiod`
* `icinga_user`
* `icinga_user_template`


Installation
------------

These modules are distributed as [collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).
To install them, run:

```
ansible-galaxy collection install T_Systems_MMS.icinga-director
```

Alternatively put the collection into a `requirements.yml`-file:

```
---
collections:
- T_Systems_MMS.icinga-director
```

Examples
--------

See the `examples` directory for a complete list of examples.

```
- hosts: localhost
  collections:
    - T_Systems_MMS.icinga-director
  tasks:
    - name: create a host in icinga
      icinga_host:
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

License
-------

GPLv3

Author Information
------------------

* Sebastian Gumprich
* Lars Krahl
