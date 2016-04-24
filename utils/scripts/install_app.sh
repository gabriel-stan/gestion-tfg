#!/bin/bash

# Script to install the application after installing system packages
# no need to run with sudo

# create and activate virtualenv
virtualenv venv
source venv/bin/activate

# get or set back requirements file
REQUIREMENTS_BACK=$1

if [ ! -f $REQUIREMENTS_BACK ]; then
    REQUIREMENTS_BACK=utils/requirements_back.txt
fi

# get or set front requirements file
REQUIREMENTS_FRONT=$2

if [ ! -f $REQUIREMENTS_FRONT ]; then
    REQUIREMENTS_FRONT=utils/requirements_front.txt
fi

# install pip requirements
pip install -r $REQUIREMENTS_BACK
pip install -r $REQUIREMENTS_FRONT

# install front requirements
nodeenv --node=4.4.0 --prebuilt venvnode
source venvnode/bin/activate

npm install -g bower
npm install
bower install

# prepare database
python manage.py syncdb --noinput
python manage.py makemigrations

# apply changes to database
python manage.py migrate

# create superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@example.com', 'gestfg')" | python manage.py shell
#python utils/scripts/createsuperuser.py


# quit virtualenv
deactivate
