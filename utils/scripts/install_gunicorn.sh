#!/bin/bash

# Script to install gunicorn after installing app
# no need to run with sudo

# activate virtualenv
source venv/bin/activate

# install pip requirements
pip install -r utils/requirements_gunicorn.txt

# quit virtualenv
deactivate
