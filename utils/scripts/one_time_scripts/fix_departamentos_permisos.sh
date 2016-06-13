#!/bin/bash

# # set or get run environment variables
ENV_VARS=$1

if [ ! -f $ENV_VARS ]; then
    ENV_VARS=utils/environment/install_env
fi

source $ENV_VARS
export $(cut -d= -f1 "$ENV_VARS")

sudo -u postgres psql -U $PGUSER -d $PGDATABASE -c "DELETE FROM auth_group_permissions;"
sudo -u postgres psql -U $PGUSER -d $PGDATABASE -c "DELETE FROM auth_permission WHERE codename='tfg.create' OR codename='evento.create';"
