#!/bin/bash

# Verify needed tools
for exec in JESftp.py; do
    if ! which $exec &> /dev/null; then
        echo You need to install $exec.
        exit 1
    fi
done


# 
# Test the mock FTP server against JESftp.py
#

testJob=testjob.jcl
outFile=outfile.txt
JESftpCFG=.JESftp.cfg

function cleanup () {
    rm $testJob $JESftpCFG $outFile
    kill %1
}
trap cleanup EXIT

# Create test job file
echo "This is testjob" > $testJob

# Create JESftp configuration
echo "[JESftp]"            > $JESftpCFG
echo "server = localhost" >> $JESftpCFG
echo "username = KC12345" >> $JESftpCFG
echo "password = webjcl"  >> $JESftpCFG

export PYTHONPATH=$PWD

python bin/zosftpd.py &
sleep 1

JESftp.py -o $outFile $testJob

# Assert
if ! diff -q $outFile $testJob; then
    echo "FTP server did not return the same job payload"
fi





