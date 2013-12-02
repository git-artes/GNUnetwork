#!/bin/bash
# mkdoc.sh: makes epydoc

EXCLUDES="viejos|otros|old|others|draft"
#EXCLUDES=${EXCLUDES}"|libfsm|libmanagement|libtimer"

if [ ! "$1" ]
then
  PRJNM=GNUnetwork
  ##echo "Usage: mkdoc.sh <project name>"
else
  PRJNM="$1"
fi
if [ -d "html" ]
then
  rm -r html/*
else 
  mkdir html
fi
echo "  excluded:" $EXCLUDES
epydoc -v --name $PRJNM --exclude $EXCLUDES .
