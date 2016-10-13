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
  deployment_path:
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


def is_valid_version(version):
    parsed_version = parse_version(version)
    if type(parsed_version) == SetuptoolsVersion:
        return version
    else:
        return None

def exec_command(module, command, cwd=None):
    rc, out, err = module.run_command(command, cwd=cwd, use_unsafe_shell=True)
    if rc != 0:
        module.fail_json(msg="Failed to issue command '%s' because stdout='%s' stderr='%s'" % (command, out, err))
    return out

def get_git_hash_dir(module, deployment_dir):
    command = "find . -maxdepth 1 -type d -exec printf '{}\n' \; | awk 'length==42' | sed 's|./||'"
    hash_dirs = exec_command(module, command, deployment_dir)
    hash_dirs = hash_dirs.split("\n")
    return hash_dirs

def get_sem_ver_dir(module, deployment_dir):
    command = "find . -maxdepth 1 -type d -exec printf '{}\n' \; | sed 's/.\|.\///'"
    hash_dirs = exec_command(module, command, deployment_dir)
    hash_dirs = hash_dirs.split("\n")

    return map(is_valid_version, hash_dirs)

def main():
    changed = False
    files_to_delete = 0
    warning = []
    module = AnsibleModule(
        argument_spec = dict(
            path      = dict(required=True, type='str'),
            keep_last = dict(required=True, type='int'),
            use_semantic_versioning = dict(default=False, required=False, type='bool'),
        ),
    )
    deployment_dir      = module.params['path']
    keep_last           = module.params['keep_last']
    semantic_versioning = module.params['use_semantic_versioning']
    # keep deployment info
    list_deployment = []
    broken_deployment_dir = []

    if semantic_versioning:
        hash_dirs = get_sem_ver_dir(module, deployment_dir)
    else:
        hash_dirs = get_git_hash_dir(module, deployment_dir)

    ## Remove empty lists
    hash_dirs = filter(None, hash_dirs)
    for hash_dir in hash_dirs:
        # Fet earliest date of deployment
        glob_path = os.path.join(deployment_dir, hash_dir,  "*.deployment.date")
        deployment_dates = glob.glob(glob_path)
        # Sort in case we have mutli deployment. We will take the oldest 1
        deployment_dates.sort()
        try:
            list_deployment.append({ "date": os.path.basename(deployment_dates[0]), "hash_dir": hash_dir })
        except IndexError:
            # Broken hash dir has no deployment_dates
            warning.append("Broken hash dir '%s' because no deployments date file(s)." % hash_dir)
            broken_deployment_dir.append({"hash_dir": hash_dir })

    # check if we execded our keep limit
    deployments2deleted = len(list_deployment) - keep_last
    if  deployments2deleted > 0:
        # Sort our list of dic with date
        list_deployment = sorted(list_deployment, key=lambda k: k['date'])
        # Get only items that will be deleted
        list_deployment = list_deployment[0:deployments2deleted]
        for dir_2_delete in list_deployment:
            changed = True
            # Remove any symlinks first inside the dir
            remove_link_cmd = "find %s -maxdepth 1 -type l -exec readlink -f {} \; | xargs rm -f" % os.path.join(deployment_dir,dir_2_delete.get("hash_dir"))
            exec_command(module, remove_link_cmd, deployment_dir)
            # Remove the dir
            remove_dir_cmd = "rm -rf %s" % os.path.join(deployment_dir,dir_2_delete.get("hash_dir"))
            exec_command(module, remove_dir_cmd, deployment_dir)

    # Check dirs that are not part of directory
    if len(broken_deployment_dir) > 0:
        for dir_2_delete in broken_deployment_dir:
            changed = True
            # Remove any symlinks first inside the dir
            remove_link_cmd = "find %s -maxdepth 1 -type l -exec readlink -f {} \; | xargs rm -f" % os.path.join(deployment_dir,dir_2_delete.get("hash_dir"))
            exec_command(module, remove_link_cmd, deployment_dir)
            # Remove the dir
            remove_dir_cmd = "rm -rf %s" % os.path.join(deployment_dir,dir_2_delete.get("hash_dir"))
            exec_command(module, remove_dir_cmd, deployment_dir)

    module.exit_json(msg="", changed=changed, deployments2deleted=deployments2deleted, list_deployment=list_deployment, broken_deployment_dir=broken_deployment_dir, warning=warning)

import glob
import os.path
import subprocess
from ansible.module_utils.basic import *
from pkg_resources import parse_version, SetuptoolsVersion
if __name__ == '__main__':
    main()

