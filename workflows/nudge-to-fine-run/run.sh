#!/bin/bash

set -e

# Will use the direnv variables for BUCKET, PROJECT, EXPERIMENT

TRIAL="v0"
TAG=${EXPERIMENT}-${TRIAL}  # required
NAME="${TAG}-$(openssl rand --hex 6)"

SEGMENTS="36"


argo submit --from workflowtemplate/prognostic-run \
    -p bucket=${BUCKET} \
    -p project=${PROJECT} \
    -p tag=${TAG} \
    -p config="$(< nudging.yaml)" \
    -p segment-count=$SEGMENTS \
    -p memory="20Gi" \
    -p cpu="24" \
    -p online-diags-flags="--verification  1yr_pire_postspinup --n-jobs 5" \
    --name "${NAME}" \
    --labels "project=${PROJECT},experiment=${EXPERIMENT},trial=${TRIAL}"
