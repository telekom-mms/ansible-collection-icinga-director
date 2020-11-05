> Code snippets that you can import to your Visual Studio Code installation

## Instruction on how to add those snippets:

```
- open VSC
- File -> Preferences -> User Snippets
- add a new one for YAML context
- paste content from yaml.json in the new file
- save the file
```

## Instruction on how to use those snippets:

For example you can type in `servicetemp` in your .yaml file and get the following output:

```yaml
- service_template_object:
    - ""
  check_command: foo
  check_interval: 60
  retry_interval: 30
  use_agent: true
```

## Change snippet prefix how you want it:

You can change the string that you need to type in to create the actual code from the snippet by changing the ```"prefix": "$Change_me,``` in your User Snippets file for your YAML code (yaml.json by default).
