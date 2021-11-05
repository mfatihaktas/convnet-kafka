#!/bin/bash

DC=docker-compose

if [ $1 = 'up' ]; then
  $DC up -d --remove-orphans
elif [ $1 = 'scale' ]; then
  $DC scale kafka=2
elif [ $1 = 'stop' ]; then
  $DC stop
elif [ $1 = 'rm' ]; then
  $DC rm
elif [ $1 = 'ls' ]; then
  $DC ps
else
  echo "Arg did not match; args= "$1
fi
