#!/bin/bash
set -e
echo "Running travis "
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

SETUP_VERSION="v0.0.3"
#SETUP_VERBOSITY="vv"


## Install Ansible 2.0
ANSIBLE_VERSIONS[0]="2.0.2.0"
INSTALL_TYPE[0]="pip"
ANSIBLE_LABEL[0]="v2"

## Install Ansible stable-2.0
ANSIBLE_VERSIONS[0]="devel"
INSTALL_TYPE[0]="git"
ANSIBLE_LABEL[0]="latest"

# Whats the default version
ANSIBLE_DEFAULT_VERSION="v2"

#
. $AVM_SETUP_PATH
