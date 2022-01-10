#!/bin/bash

# infomation
REPO=harbor.lishang4.com/lib
CONTAINER=data-science-project

GIT_HEAD="$(git rev-parse --short=7 HEAD)"
GIT_DATE=$(git log HEAD -n1 --pretty='format:%cd' --date=format:'%Y%m%d-%H%M')
TAG="${GIT_HEAD}-${GIT_DATE}"
DOCKER_IMAGE=$REPO/$CONTAINER:$TAG

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BUILDROOT=$DIR/..

# Build docker
cmd="DOCKER_BUILDKIT=1 docker build -t $DOCKER_IMAGE -f $DIR/Dockerfile $BUILDROOT"
echo $cmd
eval $cmd
