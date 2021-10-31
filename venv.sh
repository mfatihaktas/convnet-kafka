#!/bin/bash

VENV_DIR=./venv

if [ $1 = 'setup' ]; then
  python3 -m venv $VENV_DIR
elif [ $1 = 'install' ]; then
  pip3 install -r requirements.txt

  python3 convnet/setup.py bdist_wheel
  pip3 install --force-reinstall dist/convnetlib-0.1.0-py3-*.whl

  python3 kafka/setup.py bdist_wheel
  pip3 install --force-reinstall dist/kafkalib-0.1.0-py3-*.whl
elif [ $1 = 'source' ]; then
  source $VENV_DIR/bin/activate
else
  echo "Arg did not match; arg= "$1
fi
