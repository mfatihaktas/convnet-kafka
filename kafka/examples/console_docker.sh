#!/bin/bash

DOCKER=docker
COMPOSE=docker-compose

DOCKER_IT="${DOCKER} run -it --rm \
          --network kafka_app-tier \
          -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181 \
          bitnami/kafka:latest "

if [ $1 = 'kl' ]; then
  $DOCKER_IT kafka-topics.sh --list --bootstrap-server kafka:9092 --broker-list 0.0.0.0:9092
elif [ $1 = 'kp' ]; then
  $DOCKER_IT kafka-console-producer.sh --topic test --broker-list kafka:9092
elif [ $1 = 'kc' ]; then
  $DOCKER_IT kafka-console-consumer.sh --topic test --bootstrap-server kafka:9092 --from-beginning \
             --property print.key=true --property key.separator=" : "
elif [ $1 = 'kcat' ]; then
  # kcat -b localhost:9093 -t test
  kcat -b localhost:9093 -L -J | jq .
elif [ $1 = 'lsc' ]; then
  $DOCKER ps --all
elif [ $1 = 'lsn' ]; then
  $DOCKER network ls
elif [ $1 = 'lsi' ]; then
  $DOCKER images
else
  echo "Arg did not match; args= $1"
fi
