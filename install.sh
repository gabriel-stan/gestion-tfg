#!/bin/bash


virtualenv venv
source venv/bin/activate


pip install -r requirements.txt


cd gestion_tfg

python manage.py syncdb --noinput

echo "from django.contrib.autport get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

python manage.py migrate
#python manage.py migrate

deactivate

