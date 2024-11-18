#!/usr/bin/env bash

full_path=$(realpath "$0")
dir_path=$(dirname "$full_path")

for module in "$dir_path"/../plugins/modules/*.py; do

    module_name="$(basename "${module}" .py)"
    fqcn_name="telekom_mms.icinga_director.$(basename "${module}" .py)"

    if [[ $module_name == "icinga_deploy" ]]; then
      continue
    fi

    # create examples
    # https://stackoverflow.com/a/22221307
    # this greps the examples from the plugins and puts them into a temp-file
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee "/tmp/${module_name}.yml" 1> /dev/null

    if [[ $module == *info* ]]; then
      echo  "---" | \
        tee "$dir_path/../examples/${module_name}.yml" \
            "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" \
            "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" \
            "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_query_${module_name}.yml" \
            "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/no_query_${module_name}.yml" \
            1> /dev/null

      # this gets the number of lists in the module so we can iterate over them and change them
      length=$(($(yq r --length "/tmp/${module_name}.yml") - 1))
      for item in $(seq 0 ${length}); do
        # this adds the first list item to the different tests
        yq r --printMode v --collect "/tmp/${module_name}.yml" "[$item]" | \
          tee -a "$dir_path/../examples/${module_name}.yml" \
                 "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" \
                 "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" \
                 "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_query_${module_name}.yml" \
                 "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/no_query_${module_name}.yml" \
                 1> /dev/null

        # this adds an assert task that checks for response length
        # yq does this by appending the contents of "assert_info.yml"
        yq m -a -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" "$dir_path"/assert_info_found.yml
        yq m -a -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/no_query_${module_name}.yml" "$dir_path"/assert_info_found.yml
        yq m -a -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_query_${module_name}.yml" "$dir_path"/assert_info_notfound.yml

        # this adds an assert task that checks for failure
        # yq does this by appending the contents of "assert_fail.yml" to the wrong_pass/host tests
        yq m -a -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "$dir_path"/assert_fail.yml

        # this replaces the query variable with a wrong object, so nothing is found
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_query_${module_name}.yml" "(name==*).\"${fqcn_name}\".query" "noobjecttofind"

        # this replaces the password variable with a wrong password, so the login will fail
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).\"${fqcn_name}\".url_password" "iamwrong"

        # delete query to get all objects
        yq d -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/no_query_${module_name}.yml" "(name==*).\"${fqcn_name}\".query"

        # this adds ignore_errors and result-registering to the task because it will fail as expected
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).ignore_errors" "true"
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).register" "result"

        # this adds result-registering to the task because we need to assert the response
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" "(name==*).register" "result"
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_query_${module_name}.yml" "(name==*).register" "result"
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/no_query_${module_name}.yml" "(name==*).register" "result"
      done

      # this adds back three dashes that are removed when using "yq w" on the task
      sed -i '1 i ---' "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml"
      sed -i '1 i ---' "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml"
      sed -i '1 i ---' "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_query_${module_name}.yml"
      sed -i '1 i ---' "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/no_query_${module_name}.yml"
    else
      echo  "---" | \
        tee "$dir_path/../examples/${module_name}.yml" \
            "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" \
            "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" \
            "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" \
            "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" \
            1> /dev/null

      # this gets the number of lists in the module so we can iterate over them and change them
      length=$(($(yq r --length "/tmp/${module_name}.yml") - 1))
      for item in $(seq 0 ${length}); do
        # this adds the first list item to the different tests
        yq r --printMode v --collect "/tmp/${module_name}.yml" "[$item]" | \
          tee -a "$dir_path/../examples/${module_name}.yml" \
                 "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/${module_name}.yml" \
                 "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" \
                 "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" \
                 "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" \
                 1> /dev/null

        # this adds an assert task that checks for failure
        # yq does this by appending the contents of "assert_fail.yml" to the wrong_pass/host tests
        yq m -a -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "$dir_path"/assert_fail.yml
        yq m -a -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "$dir_path"/assert_fail.yml

        # this replaces "state: present" with "state: absent" in the absent_*.yml tasks
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "(name==*).\"${fqcn_name}\".state" "absent"

        # this deletes imports and command from the tests, because they aren't necessary to delete an object
        # regression test for https://github.com/telekom-mms/ansible-collection-icinga-director/issues/44
        yq d -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "(name==*).\"${fqcn_name}\".imports"
        yq d -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml" "(name==*).\"${fqcn_name}\".command"

        # this replaces the password variable with a wrong password, so the login will fail
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).\"${fqcn_name}\".url_password" "iamwrong"

        # this adds ignore_errors and result-registering to the task because it will fail as expected
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).ignore_errors" "true"
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml" "(name==*).register" "result"

        # this replaces the url variable with a nonexisting url, so the login will fail (with a different error msg than when using a wrong pw)
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "(name==*).\"${fqcn_name}\".url" "http://nonexistent"

        # this adds ignore_errors and result-registering to the task because it will fail as expected
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "(name==*).ignore_errors" "true"
        yq w -i "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml" "(name==*).register" "result"
      done

      # this adds back three dashes that are removed when using "yq w" on the task
      sed -i '1 i ---' "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_pass_${module_name}.yml"
      sed -i '1 i ---' "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/wrong_host_${module_name}.yml"
      sed -i '1 i ---' "$dir_path/../tests/integration/targets/icinga/roles/icinga/tasks/absent_${module_name}.yml"
    fi
done
