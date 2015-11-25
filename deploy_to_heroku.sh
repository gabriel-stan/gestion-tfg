#! /bin/bash

virtualenv venv

source venv/bin/activate

pip install django-toolbelt

heroku login

heroku create

git push heroku master

heroku ps:scale web=1

