#! /bin/bash

virtualenv venv

source venv/bin/activate

pip install django-toolbelt

heroku login

heroku create

heroku addons:create heroku-postgresql:hobby-dev

heroku pg:wait

git add .

git push heroku master

heroku ps:scale web=1