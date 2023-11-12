#!/usr/bin/env bash

set -e

kubectl create -f https://download.elastic.co/downloads/eck/2.10.0/crds.yaml

kubectl apply -f https://download.elastic.co/downloads/eck/2.10.0/operator.yaml
