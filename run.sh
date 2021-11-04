#!/bin/bash

PY=python3

BOOTSTRAP_SERVERS='localhost:9093'
IMG_DIR='/Users/mehmet/Desktop/convnet-kafka/convnet/examples/imgs'

if [ $1 = 's' ]; then
  [ -z "$2" ] && { echo "Server id; [0, *]?"; exit 1; }
  $PY server.py --id=$2 --bootstrap-servers=$BOOTSTRAP_SERVERS
elif [ $1 = 'c' ]; then
  [ -z "$2" ] && { echo "Client id; [0, *]?"; exit 1; }
  $PY client.py --id=$2 --img-dir=$IMG_DIR --server-ip=0.0.0.0 --server-port=8080
elif [ $1 = 'x' ]; then
  echo ""
else
  echo "Arg did not match!; args= $1, $2, $3"
fi
