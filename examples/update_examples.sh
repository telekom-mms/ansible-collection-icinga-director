#!/usr/bin/env bash

for module in ../plugins/modules/*.py; do
	module_name="$(basename ${module} .py)"

	# https://stackoverflow.com/a/22221307
	sed -n "/EXAMPLES/,/'''/{/EXAMPLES/b;/'''/b;p}" "${module}" > "${module_name}.yml"
done
