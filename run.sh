#!/bin/bash

PY=python3

BOOTSTRAP_SERVERS='localhost:9093'
TRAINING_DATA_DIR='/Users/mehmet/Desktop/fashion-mnist-data/training'
IMG_DIR='/Users/mehmet/Desktop/convnet-kafka/convnet/examples/imgs'

if [ $1 = 'c' ]; then
  [ -z "$2" ] && { echo "Client id; [0, *]?"; exit 1; }
  $PY client.py --id=$2 --img-dir=$IMG_DIR --server-ip=0.0.0.0 --server-port=5000
elif [ $1 = 's' ]; then
  [ -z "$2" ] && { echo "Server id; [0, *]?"; exit 1; }
  $PY server.py --id=$2 --bootstrap-servers=$BOOTSTRAP_SERVERS
elif [ $1 = 'cf' ]; then
  [ -z "$2" ] && { echo "Classifier id; [0, *]?"; exit 1; }
  $PY classifier.py --id=$2 --training-data-dir=$TRAINING_DATA_DIR \
                    --class-names='0,1,2,3,4,5,6,7,8,9' --bootstrap-servers=$BOOTSTRAP_SERVERS
else
  echo "Arg did not match!; args= $1, $2, $3"
fi
