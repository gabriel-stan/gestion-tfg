#!/bin/bash

wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
sudo make install
cd ../utils/
sudo ./install_server.sh
redis-server