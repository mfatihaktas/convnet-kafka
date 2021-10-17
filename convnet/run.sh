#!/bin/bash
echo $1 $2 $3

PY=python3

if [ $1 = 's' ]; then
  source ./venv/bin/activate
elif [ $1 = 'i' ]; then
  pip3 install -r requirements.txt
elif [ $1 = 'm' ]; then
  $PY model.py
elif [ $1 = 't' ]; then
  $PY test.py
elif [ $1 = 'clean' ]; then
  rm -r checkpoint/*
else
  echo "Arg did not match!"
fi
