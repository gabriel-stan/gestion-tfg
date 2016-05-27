apt-get update
apt-get install -y sudo
apt-get install -y postgresql-9.4
sudo -u postgres psql -U postgres -d postgres -c "ALTER USER postgres with password 'postgres';"
sudo -u postgres psql -U postgres -d postgres -c "ALTER ROLE postgres SET client_encoding TO 'utf8';"
sudo -u postgres psql -U postgres -d postgres -c "ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -U postgres -d postgres -c "ALTER ROLE postgres SET timezone TO 'UTC';"
sudo -u postgres psql -U postgres -d postgres -c "CREATE DATABASE gestfg"
sudo -u postgres psql -U postgres -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE gestfg TO postgres;"
