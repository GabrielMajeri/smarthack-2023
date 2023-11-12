#!/usr/bin/env bash

set -e

helm install --create-namespace --namespace harbor harbor harbor/harbor \
    --set expose.type='nodePort' \
    --set expose.tls.enabled='false' \
    --set externalURL='http://core.harbor.domain:32100' \
    --set expose.nodePort.ports.http.nodePort='32100' \
    --set persistence.resourcePolicy='' \
    --set trivy.enabled='false'
