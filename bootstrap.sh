#!/bin/sh

# make sure we have pyyaml installed

echo "checking for python-yaml..."
sudo apt list --installed python-yaml > /dev/null
if [ $? != 0 ]; then
  echo "installing..."
  sudo apt-get install python-yaml
fi

