#!/bin/bash

PY=python3
BOOTSTRAP_SERVERS='localhost:9093'

if [ $1 = 'p' ]; then
	[ -z "$2" ] && { echo "Producer id; [0, *]?"; exit 1; }
	$PY test_producer.py --id=$2 --bootstrap-servers=$BOOTSTRAP_SERVERS
elif [ $1 = 'c' ]; then
	[ -z "$2" ] && { echo "Consumer id; [0, *]?"; exit 1; }
	$PY test_consumer.py --id=$2 --group-id=0 --bootstrap-servers=$BOOTSTRAP_SERVERS
else
	echo "Arg did not match; args= $1, $2, $3"
fi
