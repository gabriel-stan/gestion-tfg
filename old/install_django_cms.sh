#Necesario estar en un virtualenv

sudo apt-get install build-essential libssl-dev libffi-dev python-dev

pip install pyopenssl ndg-httpsclient pyasn1

sudo apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev

sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/

pip install djangocms-installer

mkdir djangocms
cd djangocms

djangocms -p . mysite

