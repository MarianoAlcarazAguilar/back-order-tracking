#! /bin/bash

DOCKER_CONTAINER=$1

docker stop $DOCKER_CONTAINER
docker rm $DOCKER_CONTAINER