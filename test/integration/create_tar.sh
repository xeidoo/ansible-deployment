#!/bin/bash

app="test"

[ -z $1 ] && echo "Require a git hash" && exit 1
mkdir -p $1
touch $1/$1
tar -cvzf ${app}-$1.tar.gz $1
rm -rf $1