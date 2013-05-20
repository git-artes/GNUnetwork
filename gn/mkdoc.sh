#!/bin/bash
# mkdoc.sh: makes epydoc

EXCLUDES="viejos|otros|old|others|draft"
EXCLUDES=${EXCLUDES}"|libadaptationlayer|libfsm|libmanagement|libtimer"

if [ ! "$1" ]
then
  echo "Usage: mkdoc.sh <project name>"
else
  PRJNM="$1"
  if [ -d "html" ]
  then
    rm -r html/*
  else 
    mkdir html
  fi
  echo "  excluded:" $EXCLUDES
  epydoc -v -n $PRJNM --exclude=$EXCLUDES .
fi
