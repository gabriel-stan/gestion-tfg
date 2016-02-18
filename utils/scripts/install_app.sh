#!/bin/bash

# Script to install the application after installing system packages
# no need to run with sudo

# create and activate virtualenv
virtualenv venv
source venv/bin/activate

# install pip requirements
pip install -r utils/requirements_back.txt

# prepare database
python manage.py syncdb --noinput

# TO-DO: create superuser


# apply changes to database
python manage.py migrate

# quit virtualenv
deactivate
