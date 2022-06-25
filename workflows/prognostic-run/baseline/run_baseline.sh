#!/bin/bash

set -e

TRIAL="baseline-v0"
TAG=${EXPERIMENT}-${TRIAL}  # required
NAME="${TAG}-prog-run"

argo submit --from workflowtemplate/prognostic-run \
    -p bucket=${BUCKET} \
    -p project=${PROJECT} \
    -p tag=${TAG} \
    -p config="$(< baseline.yaml)" \
    -p segment-count=36 \
    -p memory="20Gi" \
    -p cpu="24" \
    --name "${NAME}" \
    --labels "project=${PROJECT},experiment=${EXPERIMENT},trial=${TRIAL}"

echo "argo get $NAME"