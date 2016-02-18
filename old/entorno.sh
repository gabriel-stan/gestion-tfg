#file with env vars
ENV_DIR=~/gestfg/env

source $ENV_DIR

export $(cut -d= -f1 "$ENV_DIR")

#just checking....

#echo $VARIABLE
#echo $OTRA
perl -E 'say "@ENV{qw(VARIABLE OTRA DEV)}"'
