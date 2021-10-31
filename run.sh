#!/bin/bash

PY=python3

BOOTSTRAP_SERVERS='localhost:9093'

if [ $1 = 's' ]; then
  [ -z "$2" ] && { echo "Server id; [0, *]?"; exit 1; }
  $PY server.py --id=$2 --bootstrap-servers=$BOOTSTRAP_SERVERS
elif [ $1 = 'x' ]; then
  echo ""
else
  echo "Arg did not match!; args= $1, $2, $3"
fi
