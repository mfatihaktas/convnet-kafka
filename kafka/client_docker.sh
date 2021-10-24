#!/bin/bash

# Note: container host address: docker.for.mac.localhost

DOCKER=docker
IMG=mfatihaktas/kafka-client
CONT=kafka-client
NET=kafka_app-tier

COMMON_ARGS="--net $NET \
            -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181"

if [ $1 = 'b' ]; then
  $DOCKER build -t $IMG .
elif [ $1 = 'ri' ]; then
  $DOCKER run --name $CONT -it --rm \
          $COMMON_ARGS \
          $IMG /bin/bash
elif [ $1 = 'rp' ]; then
  [ -z "$2" ] && { echo "Which producer [0, *] ?"; exit 1; }
  $DOCKER run --name producer-$2 -it --rm \
          $COMMON_ARGS \
          $IMG python3 -u /home/app/test_producer.py --i=$2
elif [ $1 = 'rc' ]; then
  [ -z "$2" ] && { echo "Which consumer [0, *] ?"; exit 1; }
  $DOCKER run --name consumer-$2 -it --rm \
          $COMMON_ARGS \
          $IMG python3 -u /home/app/test_consumer.py --i=$2
elif [ $1 = 'bash' ]; then
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
