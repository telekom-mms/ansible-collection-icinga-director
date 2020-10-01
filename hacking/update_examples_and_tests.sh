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

    yq r -d* "../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" | sponge "../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml"

    # create working tests deleting the hosts
    echo "---" | tee "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" 1> /dev/null
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee -a "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" 1> /dev/null
    yq w -d* -i "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "[].${module_name}.state" "absent"

    # delete imports and command from the tests, because they aren't necessary to delete an object
    # regression test for https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/44
    yq d -d* -i "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" ".${module_name}.imports"
    yq d -d* -i "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" ".${module_name}.command"

    yq r -d* "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" | sponge "../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml"

    # create failing tests with wrong password
    echo "---" | tee "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" 1> /dev/null
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee -a "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" 1> /dev/null

    # replace password variable with wrong password
    yq w -d* -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" ".${module_name}.url_password" "iamwrong"

    # add ignore_errors to the creation-task
    yq w -d* -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "[].ignore_errors" "true"
    yq w -d* -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "[].register" "result"

    # add an assert task that checks for failure
    yq m -d* -a -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" merge.yml

    #
    yq r -d* "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" | sponge "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml"

    # create failing tests with wrong host
    # add test
    echo "---" | tee "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" 1> /dev/null
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee -a "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" 1> /dev/null

    # replace url varuable with nonexisting url
    yq w -d* -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" ".${module_name}.url" "http://nonexistant"

    # add an assert task that checks for failure
    yq w -d* -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "[].ignore_errors" "true"

    # add ignore_errors to the creation-task
    yq w -d* -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "[].register" "result"

    # add an assert task that checks for failure
    yq m -d* -a -i "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" merge.yml

    yq r -d* "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" | sponge "../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml"

done
