#!/usr/bin/env bash

set -e

IMAGE_TAG='core.harbor.domain:32100/library/gpt-api:latest'

docker build --tag $IMAGE_TAG .

docker push $IMAGE_TAG
