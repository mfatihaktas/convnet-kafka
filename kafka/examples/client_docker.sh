#!/bin/bash

DOCKER=docker
IMG=mfatihaktas/kafka-client
CONT=kafka-client
NET=examples_app-tier

PY=python3
BOOTSTRAP_SERVERS='kafka:9092'

COMMON_DOCKER_ARGS="--net $NET \
            -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181"

if [ $1 = 'b' ]; then
  $DOCKER build -t $IMG .
elif [ $1 = 'i' ]; then
  $DOCKER run --name $CONT -it --rm \
          $COMMON_DOCKER_ARGS \
          $IMG /bin/bash
elif [ $1 = 'p' ]; then
  [ -z "$2" ] && { echo "Producer id; [0, *]?"; exit 1; }
  $DOCKER run --name producer-$2 -it --rm \
          $COMMON_DOCKER_ARGS $IMG \
          $PY -u test_producer.py --id=$2 --bootstrap-servers=$BOOTSTRAP_SERVERS
elif [ $1 = 'c' ]; then
  [ -z "$2" ] && { echo "Which consumer [0, *] ?"; exit 1; }
  $DOCKER run --name consumer-$2 -it --rm \
          $COMMON_DOCKER_ARGS $IMG \
          $PY -u test_consumer.py --id=$2 --bootstrap-servers=$BOOTSTRAP_SERVERS
elif [ $1 = 'bash' ]; then
  [ -z "$2" ] && { echo "Container?"; exit 1; }
  $DOCKER exec -it $2 bash
elif [ $1 = 'stop' ]; then
  $DOCKER stop $CONT
elif [ $1 = 'kill' ]; then
  $DOCKER kill $CONT
elif [ $1  = 'rm' ]; then
  $DOCKER rm $2
elif [ $1 = 'rmi' ]; then
  $DOCKER image rm $2
elif [ $1 = 'push' ]; then
  $DOCKER push $IMG
elif [ $1 = 'pull' ]; then
  $DOCKER pull $IMG
else
  echo "Arg did not match; args= $1, $2, $3"
fi
