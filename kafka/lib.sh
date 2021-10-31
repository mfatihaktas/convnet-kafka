#!/bin/bash

if [ $1 = 'build' ]; then
  python3 setup.py bdist_wheel
elif [ $1 = 'install' ]; then
  pip3 install -r requirements.txt
  pip3 install --force-reinstall dist/kafkalib*.whl
elif [ $1 = 'clean' ]; then
  pip3 uninstall -y -r <(pip3 freeze)
  rm -r build dist kafkalib.egg-info
elif [ $1 = 'reinstall' ]; then
  ./lib.sh clean
  ./lib.sh build
  ./lib.sh install
else
  echo "Arg did not match; args= "$1
fi
