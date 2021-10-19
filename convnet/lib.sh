#!/bin/bash

if [ $1 = 'build' ]; then
  python3 setup.py bdist_wheel
elif [ $1 = 'install' ]; then
  pip3 install --force-reinstall dist/convnetlib-0.1.0-py3-*.whl
else
  echo "Arg did not match; args= "$1
fi
