#!/bin/bash

if ! which vagrant > /dev/null; then
   
   echo "Vagrant is not installed."
   echo "Installing vagrant."

   sudo apt-get install vagrant

else
	echo "Vagrant is installed."
fi

VBOX_VERSION="$(virtualbox --help | head -n 1 | awk '{print $NF}')"

if [[ $VBOX_VERSION =~ ^4 ]]; then
	echo "VirtualBox 4.x installed."
else
	echo "Please install VirtualBox 4.x in order to continue."
	exit 1
fi

if ! which ansible > /dev/null; then
   
   echo "Ansible is not installed."
   echo "Installing ansible."

   sudo apt-get install python-pip python-dev build-essential
   sudo pip install paramiko PyYAML jinja2 httplib2 ansible

else
	echo "Ansible is installed."
fi

vagrant box add debian https://github.com/kraksoft/vagrant-box-debian/releases/download/7.8.0/debian-7.8.0-amd64.box

#vagrant init debian

vagrant up

vagrant provision