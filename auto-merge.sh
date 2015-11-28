#! /bin/bash

#curl -o /tmp/travis-automerge https://raw.githubusercontent.com/cdown/travis-automerge/master/travis-automerge
#chmod a+x /tmp/travis-automerge

printf "Travis commit message:"

echo $TRAVIS_COMMIT

git log -1

echo $TRAVIS_BRANCH

if [[ $TRAVIS_BRANCH =~ ^B ]]; then

	export BRANCHES_TO_MERGE_REGEX="$TRAVIS_BRANCH"
	export BRANCH_TO_MERGE_INTO=dev
	export GITHUB_REPO=gabriel-stan/gestion-tfg

	./travis-auto-merge.sh
elif [[ $TRAVIS_BRANCH =~ ^dev ]]; then

	export BRANCHES_TO_MERGE_REGEX="$TRAVIS_BRANCH"
	export BRANCH_TO_MERGE_INTO=master
	export GITHUB_REPO=gabriel-stan/gestion-tfg

	./travis-auto-merge.sh
fi

#BRANCHES_TO_MERGE_REGEX='^f/' BRANCH_TO_MERGE_INTO=develop GITHUB_REPO=cdown/srt /tmp/travis-automerge