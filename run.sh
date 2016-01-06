#! /bin/bash

source venv/bin/activate

cd gestion_tfg

python manage.py runserver 0.0.0.0:8000 &
