#!/bin/bash

# Script to install the application after installing system packages
# no need to run with sudo

# create and activate virtualenv
virtualenv venv
source venv/bin/activate

# get or set requirements file
REQUIREMENTS_BACK=$1

if [ ! -f $REQUIREMENTS_BACK ]; then
    REQUIREMENTS_BACK=utils/requirements_back.txt
fi

# install pip requirements
pip install -r $1

# prepare database
python manage.py syncdb --noinput
python manage.py makemigrations

# create superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'gestfg')" | python manage.py shell
#python utils/scripts/createsuperuser.py

# apply changes to database
python manage.py migrate

# quit virtualenv
deactivate
