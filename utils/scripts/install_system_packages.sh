#!/bin/bash

# System packages for the project (under Ubuntu & Debian distros)
# run with sudo

apt-get update

apt-get install -y make
apt-get install -y python python-dev python-setuptools python-pip
apt-get install -y libffi-dev libssl-dev
pip install virtualenv
