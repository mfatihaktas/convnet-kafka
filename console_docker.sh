#!/bin/bash

DC=docker
COMPOSE=docker-compose

TOPIC='img'
NET='img-net'
DC_IT="${DC} run -it --rm \
          --network $NET \
          -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181 \
          bitnami/kafka:latest "

BROKER_ADDRESS='kafka:9092'

if [ $1 = 'kl' ]; then
  $DC_IT kafka-topics.sh --list --bootstrap-server $BROKER_ADDRESS
elif [ $1 = 'kp' ]; then
  $DC_IT kafka-console-producer.sh --topic $TOPIC --broker-list $BROKER_ADDRESS \
         --property parse.key=true --property key.separator=":"
elif [ $1 = 'kc' ]; then
  $DC_IT kafka-console-consumer.sh --topic $TOPIC --bootstrap-server $BROKER_ADDRESS \
         --from-beginning --property print.key=true --property key.separator=":"
elif [ $1 = 'kcat' ]; then
  # kcat -b localhost:9093 -t test
  kcat -b localhost:9093 -L -J | jq .
elif [ $1 = 'lsc' ]; then
  $DC ps --all
elif [ $1 = 'lsn' ]; then
  $DC network ls
elif [ $1 = 'lsi' ]; then
  $DC images
else
  echo "Arg did not match; args= $1"
fi
