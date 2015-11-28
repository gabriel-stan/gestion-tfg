#! /bin/bash

#curl -o /tmp/travis-automerge https://raw.githubusercontent.com/cdown/travis-automerge/master/travis-automerge
#chmod a+x /tmp/travis-automerge

COMMIT_MESSAGE="$(git log -1 --pretty=%B)"
SYNC_DEV="*SYNC_DEV*"
SYNC_MASTER="*SYNC_MASTER*"

echo $TRAVIS_BRANCH
echo $COMMIT_MESSAGE

export COMMIT_MESSAGE

if [[ $TRAVIS_BRANCH =~ ^B ]]; then

	if [[ $COMMIT_MESSAGE == $SYNC_DEV ]] || [[ $COMMIT_MESSAGE == $SYNC_MASTER ]]; then

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

	echo "Sincronizando con BACKEND-1..."

	export BRANCHES_TO_MERGE_REGEX=dev
	export BRANCH_TO_MERGE_INTO=BACKEND-1
	export GITHUB_REPO=gabriel-stan/gestion-tfg

	./travis-auto-merge.sh

	echo "Sincronizando con BACKEND-2..."

	export BRANCHES_TO_MERGE_REGEX=dev
	export BRANCH_TO_MERGE_INTO=BACKEND-2
	export GITHUB_REPO=gabriel-stan/gestion-tfg

	./travis-auto-merge.sh

fi

#BRANCHES_TO_MERGE_REGEX='^f/' BRANCH_TO_MERGE_INTO=develop GITHUB_REPO=cdown/srt /tmp/travis-automerge