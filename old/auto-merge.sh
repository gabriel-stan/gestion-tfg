#! /bin/bash

#curl -o /tmp/travis-automerge https://raw.githubusercontent.com/cdown/travis-automerge/master/travis-automerge
#chmod a+x /tmp/travis-automerge

COMMIT_MESSAGE="$(git log -1 --pretty=%B)"

SYNC_DEV="*SYNC_DEV*"
SYNC_MASTER="*SYNC_MASTER*"

AUTO_MERGE="AUTO MERGE:"
AUTO_MERGE_REGEX="*$AUTO_MERGE*"

# solo hacer automerge en travis
if [[ $TRAVIS == 'true' ]]; then
	echo "Estoy en travis"
else
	echo "No hago auto-merge, no estoy en Travis"
	exit 0
fi

#especial para shippable (parece que no le hace caso al comando anterior...)
if [[ $USER == 'shippable' ]]; then
	echo "No hago auto-merge, estoy en Shippable"
	exit 0
else
	echo "No estoy en shippable"
fi


echo $TRAVIS_BRANCH
echo $COMMIT_MESSAGE

export COMMIT_MESSAGE
export AUTO_MERGE

if [[ $TRAVIS_BRANCH =~ ^B ]]; then

	COMMIT_MESSAGE="$COMMIT_MESSAGE from $TRAVIS_BRANCH"

	if ( [[ $COMMIT_MESSAGE == $SYNC_DEV ]] || [[ $COMMIT_MESSAGE == $SYNC_MASTER ]] ) && [[ $COMMIT_MESSAGE != $AUTO_MERGE_REGEX ]]; then

		echo "Sincronizando con DEV..."

		export BRANCHES_TO_MERGE_REGEX="$TRAVIS_BRANCH"
		export BRANCH_TO_MERGE_INTO=dev
		export GITHUB_REPO=gabriel-stan/gestion-tfg

		./travis-auto-merge.sh

	else
		echo "No se sincroniza con DEV"
	fi

elif [[ $TRAVIS_BRANCH =~ ^dev ]]; then

	if [[ $COMMIT_MESSAGE == $SYNC_MASTER ]]; then

		echo "Sincronizando con MASTER..."

		export BRANCHES_TO_MERGE_REGEX="$TRAVIS_BRANCH"
		export BRANCH_TO_MERGE_INTO=master
		export GITHUB_REPO=gabriel-stan/gestion-tfg

		./travis-auto-merge.sh

	else
		echo "No se sincroniza con MASTER"
	fi


	B1_REGEX="*$BACKEND-1*"

	if [[ $COMMIT_MESSAGE == $B1_REGEX ]]; then

		echo "No se sincroniza, viene de auto-merge de la misma rama..."

	else

		echo "Sincronizando con BACKEND-1..."

		export BRANCHES_TO_MERGE_REGEX=dev
		export BRANCH_TO_MERGE_INTO=BACKEND-1
		export GITHUB_REPO=gabriel-stan/gestion-tfg

		./travis-auto-merge.sh

	fi

	B2_REGEX="*$BACKEND-2*"

	if [[ $COMMIT_MESSAGE == $B2_REGEX ]]; then

		echo "No se sincroniza, viene de auto-merge de la misma rama..."

	else

		echo "Sincronizando con BACKEND-2..."

		export BRANCHES_TO_MERGE_REGEX=dev
		export BRANCH_TO_MERGE_INTO=BACKEND-2
		export GITHUB_REPO=gabriel-stan/gestion-tfg

		./travis-auto-merge.sh

	fi
	
fi

#BRANCHES_TO_MERGE_REGEX='^f/' BRANCH_TO_MERGE_INTO=develop GITHUB_REPO=cdown/srt /tmp/travis-automerge
