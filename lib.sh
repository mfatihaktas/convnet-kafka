#!/bin/bash

if [ $1 = 'install' ]; then
  pip3 install -r requirements.txt
  pip3 install -r convnet/requirements.txt
  pip3 install -r kafka/requirements.txt

  cd convnet
  python3 setup.py bdist_wheel
  cd ../kafka
  python3 setup.py bdist_wheel

  cd ../convnet
  pip3 install --force-reinstall dist/convnetlib-0.1.0-py3-*.whl
  cd ../kafka
  pip3 install --force-reinstall dist/kafkalib-0.1.0-py3-*.whl
elif [ $1 = 'clean' ]; then
  # pip3 uninstall -y -r <(pip3 freeze)
  pip3 uninstall convnetlib kafkalib
  # rm -r convnet/build convnet/dist convnet/convnetlib.egg-info
  # rm -r kafka/build kafka/dist kafka/kafkalib.egg-info
elif [ $1 = 'reinstall' ]; then
  ./lib.sh clean
  ./lib.sh install
else
  echo "Arg did not match; args= "$1
fi
