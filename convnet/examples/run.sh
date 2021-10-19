#!/bin/bash
echo $1 $2 $3

PY=python3

if [ $1 = 'e' ]; then
  $PY example1.py
elif [ $1 = 'clean' ]; then
  rm -r checkpoint
  rm -r log
else
  echo "Arg did not match!"
fi
