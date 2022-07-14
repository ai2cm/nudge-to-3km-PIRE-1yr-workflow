#!/bin/bash

set -e


SEGMENTS="36"



TRIAL="updated-rad-flux-ensemble"
TAG=${EXPERIMENT}-${TRIAL}  # required
NAME="${TAG}-prog-run"
argo submit --from workflowtemplate/prognostic-run \
    -p bucket=${BUCKET} \
    -p project=${PROJECT} \
    -p tag=${TAG} \
    -p config="$(< configs/ensemble.yaml)" \
    -p segment-count=$SEGMENTS \
    -p memory="25Gi" \
    -p cpu="24" \
    -p online-diags-flags="--verification  1yr_pire_postspinup --n-jobs 5" \
    --name "${NAME}" \
    --labels "project=${PROJECT},experiment=${EXPERIMENT},trial=${TRIAL}"