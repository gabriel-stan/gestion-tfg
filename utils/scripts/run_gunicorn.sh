#! /bin/bash

# # set or get run environment variables
ENV_VARS=$2

if [ ! -f $ENV_VARS ]; then
    ENV_VARS=utils/environment/run_env
fi

source $ENV_VARS
export $(cut -d= -f1 "$ENV_VARS")

# activate venv
source venv/bin/activate

# run collectstatic for static files
python manage.py collectstatic --noinput

# set gunicorn pid file to recover daemon PID later
GUNICORN_PID=gunicorn.pid

if [[ $1 != '' ]]; then
  GUNICORN_PID=$1
fi

# run with gunicorn
gunicorn gestfg.wsgi --log-file - --daemon --pid $GUNICORN_PID

# quit venv
deactivate
