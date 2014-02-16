#!/bin/bash

# Verify needed tools
for exec in virtualenv; do
    if ! which $exec &> /dev/null; then
        echo You need to install $exec.
        exit 1
    fi
done
    
TMP=/tmp/$$

function cleanup() {
    kill %1
    rm -rf $TMP
    echo DONE
}
trap cleanup EXIT

#
# Begin Test
# 

# Set up new environment
virtualenv $TMP
source $TMP/bin/activate
pip install $PWD

# Try running
zosftpd.py &
sleep 2




