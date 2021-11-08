#!/bin/bash

DC="docker compose"

if [ $1 = 'up' ]; then
  TRAINING_DATA_DIR='/Users/mehmet/Desktop/fashion-mnist-data/training' \
  CLASS_NAMES='0,1,2,3,4,5,6,7,8,9' \
  IMG_DIR='./convnet/examples/imgs' \
  $DC up -d --remove-orphans
elif [ $1 = 'scale' ]; then
  $DC scale kafka=2
elif [ $1 = 'stop' ]; then
  $DC stop
elif [ $1 = 'rm' ]; then
  $DC rm
elif [ $1 = 'down' ]; then
  ./compose.sh stop
  ./compose.sh rm
elif [ $1 = 'ls' ]; then
  $DC ps
else
  echo "Arg did not match; args= "$1
fi
