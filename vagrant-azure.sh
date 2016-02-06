#! /bin/bash

#env vars file
#$ENV_VARS=env_vars.sh
ENV_VARS=~/azure/env_vars.sh

$ENV_VARS

if [[ $# == 1 ]]; then
	vagrant $1
else
	vagrant up --provider=azure
fi

#clear env vars
> .env
