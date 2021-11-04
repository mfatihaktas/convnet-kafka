#!/bin/bash

DC=docker
IMG_NAME=mfatihaktas/img-classification-service # :latest
CONT_NAME=img-service
NET=img-net

DC_COMMON="${DC} run --rm --net ${NET}"
DC_IT="${DC_COMMON} -it"
DC_D="${DC_COMMON} -d"

KAFKA_BOOTSTRAP_SERVERS='kafka:9092'
function run_server()
{
  DC_CMD="$1"
  [ -z "$2" ] && { echo "Which server [0, *] ?"; exit 1; }
  $DC_CMD --name "server_${2}" ${IMG_NAME} \
          python3 -u /home/app/server.py --id=$2 --bootstrap-servers=$KAFKA_BOOTSTRAP_SERVERS
}

IMG_DIR='/Users/mehmet/Desktop/convnet-kafka/convnet/examples/imgs'
function run_client()
{
  DC_CMD="$1"
  [ -z "$2" ] && { echo "Which client [0, *] ?"; exit 1; }
  # echo "DC_CMD= ${DC_CMD}"
  $DC_CMD --name "client_${2}" ${IMG_NAME} \
          python3 -u /home/app/client.py --id=$2 --img-dir=$IMG_DIR --server-ip=0.0.0.0 --server-port=8080
}

function run_container()
{
  [ -z "$1" ] && { echo "Interactive (i) or as daemon (d)?"; exit 1; }
  if [ $1 = 'i' ]; then
    DC_CMD="$DC_IT"
  elif [ $1 = 'd' ]; then
    DC_CMD="$DC_D"
  fi

  [ -z "$2" ] && { echo "Client (s) or server (s)?"; exit 1; }
  if [ $2 = 'c' ]; then
    run_client "$DC_CMD" $3
  elif [ $2 = 's' ]; then
    run_server "$DC_CMD" $3
  fi
}

if [ $1 = 'b' ]; then
  rm *.png *.log
  $DC build -t $IMG_NAME .
elif [ $1 = 'bi' ]; then
  $DC_IT /bin/bash
elif [ $1 = 's' ]; then
  run_container 'i' 's' $2
  # run_container 'd' 's' $2
elif [ $1 = 'c' ]; then
  run_container 'i' 'c' $2
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
