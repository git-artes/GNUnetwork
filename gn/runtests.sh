#!/bin/bash
# runtests.sh: run Python doctest test modules
#

if [ ! -z "$1" ]
then
    DIR = $1
else
    DIR = '.'
fi

LSMODS=`ls *.txt`
for MOD in $LSMODS
  do
  echo '=== Testing' $MOD
  python -m doctest $MOD
  echo
  done
  
  


