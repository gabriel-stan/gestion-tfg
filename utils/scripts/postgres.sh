#!/bin/bash

# # set or get run environment variables
ENV_VARS=$1

if [ ! -f $ENV_VARS ]; then
    ENV_VARS=utils/environment/install_env
fi

source $ENV_VARS
export $(cut -d= -f1 "$ENV_VARS")
SCRIPTS=utils/scripts



# solo instalar pg si no estoy en travis
if [[ $TRAVIS != 'true' ]]; then
	echo "No estoy en travis"
  sudo apt-get install -y postgresql-9.4
  sudo -u postgres psql -U postgres -d postgres -c "CREATE DATABASE $PGDATABASE;"
else
	echo "No instalo postgres"
fi

sudo -u postgres psql -U postgres -d postgres -c "CREATE USER $PGUSER with password '$PGPASSWORD';"
sudo -u postgres psql -U postgres -d postgres -c "CREATE ROLE $PGUSER;"
sudo -u postgres psql -U postgres -d postgres -c "ALTER ROLE $PGUSER SET client_encoding TO 'utf8';"
sudo -u postgres psql -U postgres -d postgres -c "ALTER ROLE $PGUSER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -U postgres -d postgres -c "ALTER ROLE $PGUSER SET timezone TO 'UTC';"
sudo -u postgres psql -U postgres -d postgres -c "CREATE DATABASE $PGDATABASE;"
# sudo -u postgres psql -U postgres -d postgres --set=nombredb="$PGDATABASE" -f $SCRIPTS/create_database.sql
sudo -u postgres psql -U postgres -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $PGDATABASE TO $PGUSER;"
