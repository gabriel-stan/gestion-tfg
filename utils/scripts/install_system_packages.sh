#!/bin/bash

# System packages for the project (under Ubuntu & Debian distros)
# run with sudo

apt-get update

apt-get install -y make
apt-get install -y python python-dev python-setuptools python-pip
apt-get install -y libffi-dev libssl-dev
pip install virtualenv

# apt-get install postgresql
# sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'postgres';"
# sudo -u postgres psql -U postgres -d postgres -c "ALTER ROLE postgres SET client_encoding TO 'utf8';"
# sudo -u postgres psql -U postgres -d postgres -c "ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';"
# sudo -u postgres psql -U postgres -d postgres -c "ALTER ROLE postgres SET timezone TO 'UTC';"
# sudo -u postgres psql -U postgres -d postgres -c "CREATE DATABASE gestfg"
# sudo -u postgres psql -U postgres -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE gestfg TO postgres;"
