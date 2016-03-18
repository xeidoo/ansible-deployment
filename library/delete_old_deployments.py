#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: delete_old_deployments
version_added: 1.9
short_description: Rotate deployment directories
description:
     - The M(delete_old_deployments) module maintain a fixed number of directories in deployment path.
options:
  path:
    description:
      - Path of deployment dir 
    required: true
    default: null
  keep_last:
    description:
      - An integer that defines number of directories to keep.
    required: true
    default: null
'''

EXAMPLES = '''
# Example keep only the last three deployments
- delete_old_deployments: path=/deployments/app/ keep_last=3
'''

def exec_command(module, command, cwd=None):
    rc, out, err = module.run_command(command, cwd=cwd, use_unsafe_shell=True)
    if rc != 0:
        module.fail_json(msg="Failed to issue command '%s' because stdout='%s' stderr='%s'" % (command, out, err))
    return out

def main():
    changed = False
    files_to_delete = 0
    module = AnsibleModule(
        # not checking because of daisy chain to file module
        argument_spec = dict(
            path      = dict(required=True, type='path'), 
            keep_last = dict(required=True, type='int'),
        ),
    )
    # deployment_dir = "/Users/ahelal/Desktop/a"
    deployment_dir    = module.params['path']
    keep_last         = module.params['keep_last']

    # keep deployment info
    list_deployment = []
    command = "find . -maxdepth 1 -type d -exec printf '{}\n' \; | awk 'length==42' | sed 's|./||'"
    hash_dirs = exec_command(module, command, deployment_dir)

    hash_dirs = hash_dirs.split("\n")
    ## Removew empty lists
    hash_dirs = filter(None, hash_dirs) 
    for hash_dir in hash_dirs:
        # get earliest date of deployment 
        glob_path = os.path.join(deployment_dir, hash_dir,  "*.deployment.date")
        deployment_dates = glob.glob(glob_path)
        # Sort in case we have mutli deployment and we will take the oldest 
        deployment_dates.sort()
        list_deployment.append({ "date": os.path.basename(deployment_dates[0]), "hash_dir": hash_dir })

    # check if we execded our limit
    deployments2deleted = len(list_deployment) - keep_last
    if  deployments2deleted > 0:
        # We need to sort our list of dic with date in order to remoe the oldest
        list_deployment = sorted(list_deployment, key=lambda k: k['date'])
        # Get only items that will be deleted
        list_deployment = list_deployment[0:deployments2deleted]:
        for dir_2_delete in list_deployment[0:deployments2deleted]:
            changed = True 
            # Remove any symlinks first inside the dir
            remove_link_cmd = "find %s -type l -delete" % os.path.join(deployment_dir,dir_2_delete.get("hash_dir"))
            exec_command(module, remove_link_cmd, deployment_dir)
            # Remove the dir
            remove_dir_cmd = "rm -rf %s" % os.path.join(deployment_dir,dir_2_delete.get("hash_dir"))
            exec_command(module, remove_dir_cmd, deployment_dir)

    module.exit_json(msg="", changed=changed, deployments2deleted=deployments2deleted, list_deployment=list_deployment)

import glob
import os.path
import subprocess
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()

