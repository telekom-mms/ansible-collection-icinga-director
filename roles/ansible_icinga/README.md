# Ansible Icinga

This role is used to configure an Icinga Instance over its Icinga Director.

## Installation

* create a `requirements.yml`:

```bash
---
collections:
  - name: t_systems_mms.icinga_director
    src: https://github.com/T-Systems-MMS/ansible-collection-icinga-director
    version: 1.2.2
```

* install the collections:

```bash
ansible-galaxy collection install -r requirements.yml -p collections/
```

## Dependencies

collections:
t_systems_mms.icinga_director >= 1.2.2

## Role Variables

| Variable                         | Required | Default                     |
| -------------------------------- | -------- | --------------------------- |
| **icinga**                       |
| url                              | true     |
| use_proxy                        | false    |
| validate_certs                   | false    |
| url_username                     | true     |
| url_password                     | true     |
| force_basic_auth                 | false    |
| client_cert                      | false    |
| client_key                       | false    |
| **icinga_timeperiod**            |
| icinga_timeperiods               | false    | []                          |
| display_name                     | false    |
| imports                          | false    |
| ranges                           | false    |
| **icinga_user_template**         |
| icinga_user_templates            | false    | []                          |
| imports                          | false    |
| period                           | false    |
| enable_notifications             | false    |
| **icinga_user**                  |
| icinga_users                     | false    | []                          |
| display_name                     | false    |
| imports                          | true     | []                          |
| pager                            | false    |
| period                           | false    |
| disabled                         | false    |
| email                            | true     | null                        |
| **icinga_zone**                  |
| icinga_zones                     | false    | []                          |
| is_global                        | false    |
| parent                           | false    |
| **icinga_endpoint**              |
| icinga_endpoints                 | false    | []                          |
| host                             | false    |
| port                             | false    |
| log_duration                     | false    |
| zone                             | false    |
| **icinga_hostgroup**             |
| icinga_hostgroups                | false    | []                          |
| display_name                     | false    |
| assign_filter                    | false    | `host.name="hostgroup.1-*"` |
| **icinga_host_template**         |
| icinga_host_templates            | false    | []                          |
| display_name                     | false    |
| address                          | false    |
| address6                         | false    |
| groups                           | false    |
| check_command                    | false    |
| check_interval                   | false    |
| disabled                         | false    |
| imports                          | false    |
| zone                             | false    |
| vars                             | false    |
| notes                            | false    |
| notes_url                        | false    |
| **icinga_host**                  |
| icinga_hosts                     | false    | []                          |
| display_name                     | false    |
| address                          | false    |
| address6                         | false    |
| groups                           | false    |
| disabled                         | false    |
| imports                          | true     | []                          |
| zone                             | false    |
| vars                             | false    |
| notes                            | false    |
| notes_url                        | false    |
| **icinga_command_template**      |
| icinga_command_templates         | false    | []                          |
| display_name                     | false    |
| command                          | false    |
| methods_execute                  | true     | PluginCheck                 |
| timeout                          | false    |
| imports                          | false    |
| disabled                         | false    |
| zone                             | false    |
| vars                             | false    |
| arguments                        | false    |
| **icinga_command**               |
| icinga_commands                  | false    | []                          |
| command_type                     | true     | PluginCheck                 |
| disabled                         | true     | false                       |
| imports                          | false    |
| zone                             | false    |
| vars                             | false    |
| **icinga_service**               |
| icinga_services                  | false    | []                          |
| display_name                     | false    |
| disabled                         | false    |
| check_command                    | false    |
| check_interval                   | false    |
| check_period                     | false    |
| check_timeout                    | false    |
| enable_active_checks             | false    |
| enable_event_handler             | false    |
| enable_notifications             | false    |
| enable_passive_checks            | false    |
| enable_perfdata                  | false    |
| groups                           | false    |
| host                             | true     |
| imports                          | false    |
| max_check_attempts               | false    |
| notes                            | false    |
| notes_url                        | false    |
| retry_interval                   | false    |
| use_agent                        | false    |
| vars                             | false    |
| volatile                         | false    |
| **icinga_service_template**      |
| icinga_service_templates         | false    | []                          |
| display_name                     | false    |
| disabled                         | false    |
| check_command                    | false    |
| check_interval                   | false    |
| check_period                     | false    |
| check_timeout                    | false    |
| enable_active_checks             | false    |
| enable_event_handler             | false    |
| enable_notifications             | false    |
| enable_passive_checks            | false    |
| enable_perfdata                  | false    |
| groups                           | false    |
| imports                          | false    |
| max_check_attempts               | false    |
| notes                            | false    |
| notes_url                        | false    |
| retry_interval                   | false    |
| use_agent                        | false    |
| vars                             | false    |
| volatile                         | false    |
| **icinga_service_apply**         |
| icinga_service_applys            | false    | []                          |
| display_name                     | false    |
| groups                           | false    |
| apply_for                        | false    |
| assign_filter                    | false    |
| imports                          | false    |
| vars                             | false    |
| notes                            | false    |
| notes_url                        | false    |
| **icinga_servicegroup**          |
| icinga_servicegroups             | false    | []                          |
| display_name                     | false    |
| assign_filter                    | false    |
| **icinga_notification_template** |
| icinga_notification_templates    | false    | []                          |
| notification_template_object     | false    |
| state                            | false    |
| notification_interval            | false    |
| states                           | false    |
| types                            | false    |
| times_begin                      | false    |
| times_end                        | false    |
| timeperiod                       | false    |
| users                            | false    |
| user_groups                      | false    |
| notification_command             | false    |
| imports                          | false    |
| **icinga_notification**          |
| icinga_notifications             | false    | []                          |
| notification_interval            | false    |
| types                            | false    |
| users                            | false    |
| apply_to                         | false    |
| assign_filter                    | false    |
| imports                          | false    |
| period                           | false    |
| **icinga_scheduled_downtime**    |
| icinga_scheduled_downtimes       | false    | []                          |
| state                            | true     | present
| disabled                         | false    | false
| assign_filter                    | false    |
| apply_to                         | true     |
| author                           | true     |
| comment                          | true     |
| duration                         | false    |
| fixed                            | true     |
| ranges                           | false    |
| with_services                    | false    | true

## Example Playbook

```bash
---
- hosts: localhost
  gather_facts: false
  collections:
  - t_systems_mms.icinga_director
  roles:
    - ansible_icinga
  vars:
    icinga_url: "https://example.com"
    icinga_user: "{{ icinga_user }}"
    icinga_pass: "{{ icinga_pass }}"
    icinga_timeperiods:
      - timeperiod_object:
        - "8x5"
        ranges:
          monday: "09:00-17:00"
          tuesday: "09:00-17:00"
          wednesday: "09:00-17:00"
          thursday: "09:00-17:00"
          friday: "09:00-17:00"
      - timeperiod_object:
        - "24x7"
        ranges:
          monday: "00:00-24:00"
          tuesday: "00:00-24:00"
          wednesday: "00:00-24:00"
          thursday: "00:00-24:00"
          friday: "00:00-24:00"
          saturday: "00:00-24:00"
          sunday: "00:00-24:00"
    icinga_users:
      - user_object:
        - "service_abbreviation_email_24x7"
        pager: "SIP/xxx"
        email: "service_abbreviation@example.com"
      - user_object:
        - "service_abbreviation_8x5"
        email: "service_abbreviation@example.com"
    icinga_hostgroups:
      - hostgroup_object:
        - "service_abbreviation-environement"
        - "service_abbreviation-environement-web"
    icinga_hosts:
      - host_object:
        - "service_abbreviation-environement-web01"
    icinga_scheduled_downtimes:
      - scheduled_downtime_object:
        - "service_abbreviation-environement-downtime01"
```
