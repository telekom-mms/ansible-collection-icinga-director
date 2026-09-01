Icinga Director Ansible Playbooks
================================

Introduction
------------

This document provides an illustrative guide to managing services in Icinga Director using sample Ansible playbooks in the example directory which leverage the `telekom_mms.icinga_director` Ansible collection.
These playbooks described here are intended as examples, designed to demonstrate potential use cases and provide a basis for custom playbook development.
It's important to note that these examples are not meant to be deployed without modifications and made to fit a specific environment, so your requirements may differ.
These playbooks include management for the lifecycle of icinga object, including creation, update and delete, to make the Ansible configuration the SPoT.

Due to the behaviour of Ansible and the Icinga Director API, there are some workarounds chosen in these playbooks, especially to enable implicit deletion of objects.



How to Use
----------


The playbook includes three tasks and a role that is executed thereafter:

1. **Include Vars**: This task includes variables from the `vars/icinga_{object}.yml` file. Object is the general Term for different Icinga Director objects like services, hosts, etc.

2. **Get All Object Configs**: This task retrieves all object configurations from the Icinga Director. The `url`, `url_username`, and `url_password` variables are used to authenticate with the Icinga Director. The `query` variable is set to `"*"` to retrieve all object configurations. The result is registered in the `result` variable.

3. **Create Objects Scheduled for Deletion**: This task creates objects that are scheduled for deletion. The `icinga_{object}` variable is updated with the Objects in the Icinga Director
      that are not currently in the `icinga_{object}` list.
      This means that any object that exists in the Director, but is not defined in the playbook will be marked for deletion.
      This done by creating objects with an `'absent'` state to remove them and define in the configuration as the SPoT.

In addition to these tasks, the playbook uses the `ansible_icinga` role.

Variables
---------

The playbook uses the following variables:

- `icinga_host`: The URL of the Icinga Director.
- `icinga_user`: The username used for authentication with the Icinga Director.
- `icinga_pass`: The password used for authentication with the Icinga Director.
- `icinga_{object}`: A list of objects different by type managed by the playbook. This variable should be defined in the `vars/icinga_service.yml` file.
- `icinga_delete`: This variable controls whether objects not defined in the vars should be deleted from the Icinga Director. Currently it is set to `false` by default.

Make sure to define these variables before running the playbook.

Running the Playbook
--------------------

To run the playbook, use the `ansible-playbook` command.:

.. code-block:: bash

   ansible-playbook  icinga_{object}.yml

To run all playbooks at once there is a meta playbook to. 
This playbook will execute all example playbooks sequentially and execution is controlled by the tags, too.
Additionally, it is possible to customize the example playbook runs if needed.
This is achieved by adjusting the tags. By setting the `icinga_delete` tag you can enable or disable the deletion of objects.
