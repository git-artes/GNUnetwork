#!/bin/bash
#
# rundoctests.sh: corre como doctest todos los archivos *.txt

LSFILES=`ls -1 *.txt`
for FILE in $LSFILES
do
    echo "===  $FILE  ==="
    python -m doctest $FILE
    echo
done

