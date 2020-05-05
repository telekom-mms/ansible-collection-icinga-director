Ansible Icinga Modules
=========

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


Examples
--------

See the `examples` directory for a complete list of examples.

```
- hosts: localhost
  roles:
    - ansible-icinga-modules
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
