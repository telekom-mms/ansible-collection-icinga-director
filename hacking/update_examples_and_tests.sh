#!/usr/bin/env bash

for module in ../plugins/modules/*.py; do
    module_name="$(basename "${module}" .py)"

    # create examples
    # https://stackoverflow.com/a/22221307
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee "/tmp/${module_name}.yml" 1> /dev/null
    length=$(($(yq r --length "/tmp/${module_name}.yml") - 1))

    echo  "---" | tee "../examples/${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" 1> /dev/null

    for item in $(seq 0 ${length}); do
      yq r --printMode v --collect "/tmp/${module_name}.yml" "[$item]" | tee -a "../examples/${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" 1> /dev/null

      # add an assert task that checks for failure
      yq m -a -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" merge.yml
      yq m -a -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" merge.yml

      # create working tests deleting the hosts
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "(name==*).${module_name}.state" "absent"

      # delete imports and command from the tests, because they aren't necessary to delete an object
      # regression test for https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/44
      yq d -i "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "(name==*).${module_name}.imports"
      yq d -i "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "(name==*).${module_name}.command"

      # create failing tests with wrong password
      # replace password variable with wrong password
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).${module_name}.url_password" "iamwrong"

      # add ignore_errors to the creation-task
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).ignore_errors" "true"
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).register" "result"

      # create failing tests with wrong host
      # replace url varuable with nonexisting url
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "(name==*).${module_name}.url" "http://nonexistant"

      # add an assert task that checks for failure
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "(name==*).ignore_errors" "true"

      # add ignore_errors to the creation-task
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "(name==*).register" "result"

    done
      sed -i '1 i ---' "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml"
      sed -i '1 i ---' "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml"
      sed -i '1 i ---' "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml"
done
