#!/bin/bash
# At this point, the parent dir of .ops is the checked out repo
set -e
set -u
RUNNING=$0 # generally assumed to be run as <checkout dir> $ .ops/docker-build.sh
TAG=$1
THISDIR=$(echo $PWD/$(dirname $0))
WORKDIR=$(dirname $THISDIR)
cd $WORKDIR
scripts/echo_version_json.sh > ./leaderboard/version.json
tar --exclude .ops --exclude .git -c -f - . | docker build -t $TAG -f ./Dockerfile - 
