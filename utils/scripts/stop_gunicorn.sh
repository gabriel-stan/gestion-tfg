#! /bin/bash

# get or set default gunicorn PID file to kill daemon
GUNICORN_PID=gunicorn.pid

if [[ $1 != '' ]]; then
  GUNICORN_PID=$1
fi

# kill gunicorn daemon
kill `cat $GUNICORN_PID`
