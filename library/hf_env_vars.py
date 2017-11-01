#!/usr/bin/python
import filecmp
import grp
import os
import pwd
import shutil
import tempfile

from ansible.module_utils.basic import *


def main():
    module_args = dict(
        owner=dict(type='str', required=True),
        group=dict(type='str', required=True),
        mode=dict(type='str', required=True),
        vars=dict(type='list', required=True),
        template=dict(type='str', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    template = module.params['template']

    result = dict(
        changed=False,
    )

    try:
        tempdir = tempfile.mkdtemp()
        uid = pwd.getpwnam(module.params['owner']).pw_uid
        gid = grp.getgrnam(module.params['group']).gr_gid

        for vars_block in module.params['vars']:
            old_vars_path = vars_block['dest']
            new_vars_path = os.path.join(
                tempdir,
                os.path.basename(vars_block['dest'])
            )

            # Write new var file to tmp
            with open(new_vars_path, 'w') as f:
                f.write("# Ansible managed, Don't modify manually\n\n")

                for var_name in vars_block['vars']:
                    line = template.format(
                        var_name=var_name,
                        var_value=str(vars_block['vars'][var_name])
                    )
                    f.write(line)

            # Compare old and new file
            if os.path.isfile(old_vars_path):
                # compare file content
                if not filecmp.cmp(new_vars_path, old_vars_path):
                    result['changed'] = True
                # compare file stat (group, user, mode)
                else:
                    fstat = os.stat(old_vars_path)
                    if not fstat.st_uid == uid:
                        result['changed'] = True
                    elif not fstat.st_gid == gid:
                        result['changed'] = True
                    elif not bool(fstat.st_mode & int(module.params['mode'], 8)):
                        result['changed'] = True
            else:
                result['changed'] = True

            # Copy the temp file if something changed
            if result['changed']:
                shutil.move(new_vars_path, old_vars_path)
                os.chown(old_vars_path, uid, gid)
                os.chmod(old_vars_path, int(module.params['mode'], 8))
    finally:
        shutil.rmtree(tempdir)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
