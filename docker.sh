#!/bin/bash

DC=docker
IMG_NAME=mfatihaktas/img-classification-service # :latest
CONT_NAME=img-service
NET_NAME=convnet-kafka_img-net

DC_IT="$DC run --name $CONT_NAME -it --rm --net $NET_NAME $IMG_NAME"
DC_D="$DC run --name $CONT_NAME -d --rm --net $NET_NAME $IMG_NAME"
KAFKA_BOOTSTRAP_SERVERS='kafka:9092'

if [ $1 = 'b' ]; then
  rm *.png *.log
  $DC build -t $IMG_NAME .
elif [ $1 = 'ib' ]; then
  $DC_IT /bin/bash
elif [ $1 = 'i' ]; then
  [ -z "$2" ] && { echo "Which server [0, *] ?"; exit 1; }
  $DC_IT python3 -u /home/app/server.py --id=$2 --bootstrap-servers=$KAFKA_BOOTSTRAP_SERVERS
elif [ $1 = 'd' ]; then
  [ -z "$2" ] && { echo "Which server [0, *] ?"; exit 1; }
  $DC_D python3 -u /home/app/server.py --id=$2 --bootstrap-servers=$KAFKA_BOOTSTRAP_SERVERS
elif [ $1 = 'stop' ]; then
  $DC stop $CONT_NAME
elif [ $1 = 'kill' ]; then
  $DC kill $CONT_NAME
elif [ $1 = 'bash' ]; then
  # $DC exec -it $CONT_NAME bash
  $DC exec -it $2 bash
elif [ $1 = 'lsc' ]; then
  $DC ps --all
elif [ $1 = 'lsi' ]; then
  $DC images
elif [ $1  = 'tag' ]; then
  $DC tag $IMG_NAME $HUB_IMG_NAME
elif [ $1  = 'rm' ]; then
  $DC rm $2
elif [ $1 = 'rmi' ]; then
  $DC image rm $2
elif [ $1 = 'push' ]; then
  $DC push $IMG_NAME
elif [ $1 = 'pull' ]; then
  $DC pull $IMG_NAME
else
  echo "Arg did not match!"
fi
