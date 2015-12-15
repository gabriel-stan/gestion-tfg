#!/bin/bash

sudo apt-get install -y python python-dev python-distribute python-pip
sudo apt-get install -y postgresql postgresql-contrib libpq-dev
sudo apt-get install -y python-dev libffi-dev libssl-dev curl

pip install virtualenv

virtualenv venv
source venv/bin/activate

pip install pyopenssl ndg-httpsclient pyasn1

pip install -r requirements.txt

cd gestion_tfg

python manage.py migrate

deactivate

