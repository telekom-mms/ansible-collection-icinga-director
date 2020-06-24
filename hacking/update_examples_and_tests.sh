#!/usr/bin/env bash

for module in ../plugins/modules/*.py; do
    module_name="$(basename "${module}" .py)"

    echo "---" | tee "../tests/integration/${module_name}.yml" "../examples/${module_name}.yml"
    # https://stackoverflow.com/a/22221307
    sed -n '/EXAMPLES/,/"""/{/EXAMPLES/b;/"""/b;p}' "${module}" | tee -a "../examples/${module_name}.yml" "../tests/integration/${module_name}.yml"
done
