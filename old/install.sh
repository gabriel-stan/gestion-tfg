#!/bin/bash


virtualenv venv
source venv/bin/activate


pip install -r requirements.txt


cd gestion_tfg

python manage.py syncdb --noinput

#create an initial user for admin interface, change password on first connection recommended
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'gestfg')" | python manage.py shell

python manage.py migrate
#python manage.py migrate

deactivate
