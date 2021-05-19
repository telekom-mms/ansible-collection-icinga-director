We accept all kinds of contributions, whether they are bug fixes, pull requests or documentation updates!

If you want to develop new content for this collection or improve what is already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATH`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

For example, if you are working in the `~/dev` directory:

```
cd ~/dev
git clone https://github.com/T-Systems-MMS/ansible-collection-icinga-director collections/ansible_collections/t_systems_mms/icinga_director
export COLLECTIONS_PATH=$(pwd)/collections:$COLLECTIONS_PATH
```

You can find more information in the [developer guide for collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections), and in the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html).
