#!/bin/bash

pip install virtualenv


virtualenv venv
source venv/bin/activate


pip install -r requirements.txt


cd gestion_tfg

python manage.py syncdb --noinput
python manage.py migrate
python manage.py migrate

deactivate

