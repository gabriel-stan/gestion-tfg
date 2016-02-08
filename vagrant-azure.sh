#! /bin/bash

#env vars file
#$ENV_VARS=env_vars.sh
ENV_VARS=~/azure/env_vars.sh

$ENV_VARS

if [[ $# == 1 ]]; then

	if [[ $1 == 'norun' ]]; then

		#head -n -1 .env > .env.tmp ; mv .env.tmp .env

		echo SKIP_TAGS="--skip-tags=runserver" >> .env
		
		vagrant up --provider=azure

		#$FABRIC="fa -p '$VM_PASS' -H '$VM_USER'@'$VM_NAME'.cloudapp.net run_app"

	else
		vagrant $1
	fi
else
	vagrant up --provider=azure
fi

#clear env vars
> .env
