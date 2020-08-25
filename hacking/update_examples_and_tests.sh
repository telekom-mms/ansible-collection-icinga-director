#!/usr/bin/env bash

for module in ../plugins/modules/*.py; do
    module_name="$(basename "${module}" .py)"

    # create examples and create working tests
    echo "---" | tee "../tests/integration/targets/icinga/tasks/${module_name}.yml" "../examples/${module_name}.yml"
    # https://stackoverflow.com/a/22221307
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee -a "../examples/${module_name}.yml" "../tests/integration/targets/icinga/tasks/${module_name}.yml"

    # create failing tests with wrong password
    # add test
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee "../tests/integration/targets/icinga/tasks/wrong_pass_${module_name}.yml"
    # replace password variable with wrong password
    sed -i 's/{{ icinga_pass }}/iamwrong/g' "../tests/integration/targets/icinga/tasks/wrong_pass_${module_name}.yml"

    # add ignore_errors to the creation-task and an assert task that checks for failure
    echo -n "
  ignore_errors: true
  register: result

- name: assert that the previous task failed with 401
  assert:
    that:
      - \"result.failed\"
      - \"result.msg == 'bad return code while creating: 401. Error message: HTTP Error 401: Unauthorized'\"  # noqa" >> "../tests/integration/targets/icinga/tasks/wrong_pass_${module_name}.yml"

    # create failing tests with wrong host
    # add test
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee "../tests/integration/targets/icinga/tasks/wrong_host_${module_name}.yml"
    # replace url varuable with nonexisting url
    sed -i 's/{{ icinga_url }}/http:\/\/nonexistant/g' "../tests/integration/targets/icinga/tasks/wrong_host_${module_name}.yml"

    # add ignore_errors to the creation-task and an assert task that checks for failure
    echo -n "
  ignore_errors: true
  register: result

- name: assert that the previous task failed with 401
  assert:
    that:
      - \"result.failed\"
      - \"result.msg == 'bad return code while creating: -1. Error message: Request failed: <urlopen error [Errno -3] Temporary failure in name resolution>'\"  # noqa" >> "../tests/integration/targets/icinga/tasks/wrong_host_${module_name}.yml"
done
