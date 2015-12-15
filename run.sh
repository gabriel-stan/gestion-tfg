#! /bin/bash

source venv/bin/activate

cd gestion_tfg

python manage.py migrate

python manage.py runserver