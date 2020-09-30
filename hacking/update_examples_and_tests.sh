#!/usr/bin/env bash

for module in ../plugins/modules/*.py; do
    module_name="$(basename "${module}" .py)"

    # create examples
    echo "---" | tee "../examples/${module_name}.yml" 1> /dev/null
    # https://stackoverflow.com/a/22221307
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee -a "../examples/${module_name}.yml" 1> /dev/null

    # create tests
    echo "---" | tee "../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" 1> /dev/null
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee -a "../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" 1> /dev/null

    # create working tests deleting the hosts
    echo "---" | tee "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" 1> /dev/null
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee -a "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" 1> /dev/null
    sed -i 's/state: present/state: absent/g' "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml"
    sed -i '/imports:/,+1d' "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml"
    sed -i '/^\s*command:/d' "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml"

    # create failing tests with wrong password
    echo "---" | tee "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" 1> /dev/null
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee -a "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" 1> /dev/null
    # replace password variable with wrong password
    sed -i 's/{{ icinga_pass }}/iamwrong/g' "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml"

    # add ignore_errors to the creation-task and an assert task that checks for failure
    echo -n "
  ignore_errors: true
  register: result

- name: assert that the previous task failed with 401
  assert:
    that:
      - \"result.failed\"
      - \"result.msg == 'bad return code while creating: 401. Error message: HTTP Error 401: Unauthorized' or result.msg == 'bad return code while creating: -1. Error message: Request failed: <urlopen error [Errno -3] Temporary failure in name resolution>' or result.msg == 'bad return code while creating: -1. Error message: Request failed: <urlopen error [Errno -2] Name or service not known>'\"  # noqa
" >> "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml"

    # create failing tests with wrong host
    # add test
    echo "---" | tee "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" 1> /dev/null
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee -a "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" 1> /dev/null
    # replace url varuable with nonexisting url
    sed -i 's/{{ icinga_url }}/http:\/\/nonexistant/g' "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml"

    # add ignore_errors to the creation-task and an assert task that checks for failure
    echo -n "
  ignore_errors: true
  register: result

- name: assert that the previous task failed with 401
  assert:
    that:
      - \"result.failed\"
      - \"result.msg == 'bad return code while creating: 401. Error message: HTTP Error 401: Unauthorized' or result.msg == 'bad return code while creating: -1. Error message: Request failed: <urlopen error [Errno -3] Temporary failure in name resolution>' or result.msg == 'bad return code while creating: -1. Error message: Request failed: <urlopen error [Errno -2] Name or service not known>'\"  # noqa
" >> "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml"
done
