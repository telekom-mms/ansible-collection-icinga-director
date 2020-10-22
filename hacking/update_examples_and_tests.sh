#!/usr/bin/env bash

for module in ../plugins/modules/*.py; do
    module_name="$(basename "${module}" .py)"

    # create examples
    # https://stackoverflow.com/a/22221307
    # this greps the examples from the plugins and puts them into a temp-file
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee "/tmp/${module_name}.yml" 1> /dev/null
    # this gets the number of lists in the module so we can interate over them and change them
    length=$(($(yq r --length "/tmp/${module_name}.yml") - 1))

    echo  "---" | tee "../examples/${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" 1> /dev/null

    for item in $(seq 0 ${length}); do
      # this adds the first list item to the different tests
      yq r --printMode v --collect "/tmp/${module_name}.yml" "[$item]" | tee -a "../examples/${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" 1> /dev/null

      # this adds an assert task that checks for failure
      # yq does this by appending the contents of "merge.yml" to the wrong_pass/host tests
      yq m -a -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" merge.yml
      yq m -a -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" merge.yml

      # this replaces "state: present" with "state: absent" in the absent_*.yml tasks
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "(name==*).${module_name}.state" "absent"

      # this deletes imports and command from the tests, because they aren't necessary to delete an object
      # regression test for https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/44
      yq d -i "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "(name==*).${module_name}.imports"
      yq d -i "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "(name==*).${module_name}.command"

      # this replaces the password variable with a wrong password, so the login will fail
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).${module_name}.url_password" "iamwrong"

      # this adds ignore_errors and result-registering to the task because it will fail as expected
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).ignore_errors" "true"
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).register" "result"

      # this replaces the url variable with a nonexisting url, so the login will fail (with a different error msg than when using a wrong pw)
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "(name==*).${module_name}.url" "http://nonexistant"

      # this adds ignore_errors and result-registering to the task because it will fail as expected
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "(name==*).ignore_errors" "true"
      yq w -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "(name==*).register" "result"

    done
      # this adds back three dashes that are removed when using "yq w" on the task
      sed -i '1 i ---' "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml"
      sed -i '1 i ---' "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml"
      sed -i '1 i ---' "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml"
done
