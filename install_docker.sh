#! /bin/bash

sudo apt-get update

sudo apt-get install -y docker.io

sudo docker pull gabrielstan/gestfg

sudo docker run gabrielstan/gestfg
