#! /bin/bash

#set project root folder (or where Vagrantfile is)
ROOT_FOLDER=.

echo MGMT_CERT="/cert/file.pem" > $ROOT_FOLDER/.env
echo SUBSCR_ID="your-subscription-id" >> $ROOT_FOLDER/.env

echo VM_NAME="vm-name" >> $ROOT_FOLDER/.env
echo VM_IMAGE="vm-image" >> $ROOT_FOLDER/.env
#echo VM_IMAGE="b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150506-en-us-30GB" >> $ROOT_FOLDER/.env

echo CLOUD_SERVICE_NAME="your-cloud-service-name" >> $ROOT_FOLDER/.env
echo CLOUD_STORAGE_NAME="your-cloud-storage-name" >> $ROOT_FOLDER/.env

echo VM_SIZE="size" >> $ROOT_FOLDER/.env
echo BOX_URL="box-url" >> $ROOT_FOLDER/.env
#echo VM_SIZE="Small" >> $ROOT_FOLDER/.env
#echo BOX_URL="https://github.com/msopentech/vagrant-azure/raw/master/dummy.box" >> $ROOT_FOLDER/.env

echo VM_USER="vm-username" >> $ROOT_FOLDER/.env
echo VM_PASS="vm-pass" >> $ROOT_FOLDER/.env

echo VM_LOCATION="location" >> $ROOT_FOLDER/.env
#echo VM_LOCATION="North Europe" >> $ROOT_FOLDER/.env


#usually the same as above
echo SSH_USER="vm-username" >> $ROOT_FOLDER/.env
echo SSH_PASS="vm-pass" >> $ROOT_FOLDER/.env

