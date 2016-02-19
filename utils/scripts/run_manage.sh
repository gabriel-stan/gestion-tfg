#! /bin/bash

# set or get run environment variables
ENV_VARS=$1

if [ ! -f $ENV_VARS ]; then
    ENV_VARS=utils/environment/run_env
fi

source $ENV_VARS
export $(cut -d= -f1 "$ENV_VARS")

# activate venv
source venv/bin/activate

# run with manage.py
python manage.py runserver 8000 &

# quit venv
deactivate
