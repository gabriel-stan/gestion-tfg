#!/bin/bash

sudo apt-get install -y python python-dev python-distribute python-pip
sudo apt-get install -y postgresql postgresql-contrib libpq-dev
sudo apt-get install -y python-dev libffi-dev libssl-dev curl

sudo pip install virtualenv