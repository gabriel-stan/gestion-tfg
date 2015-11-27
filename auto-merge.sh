#! /bin/bash

#curl -o /tmp/travis-automerge https://raw.githubusercontent.com/cdown/travis-automerge/master/travis-automerge
#chmod a+x /tmp/travis-automerge


echo $TRAVIS_BRANCH

#BRANCHES_TO_MERGE_REGEX='^f/' BRANCH_TO_MERGE_INTO=develop GITHUB_REPO=cdown/srt /tmp/travis-automerge