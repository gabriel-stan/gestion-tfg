#!/bin/bash
#ejecutar con source
echo "Instalamos virtualenv"
pip install virtualenv

cd ~
mkdir gestion_tfg
cd gestion_tfg

mkdir venv_entorno

virtualenv venv_entorno
source venv_entorno/bin/activate

echo "Actualizamos el sistema"
sudo apt-get update

echo "Instalamos git"
sudo apt-get install git

cd ~
echo "Descargando entornos"
cd gestion_tfg

git clone https://github.com/gabriel-stan/gestion-tfg.git



