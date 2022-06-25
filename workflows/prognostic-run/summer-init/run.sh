#!/bin/bash

set -e


SEGMENTS="4"

for i in {0..0}
do
    TRIAL="summer-init-v0"
    TAG=${EXPERIMENT}-${TRIAL}  # required
    NAME="${TAG}-prog-run"
    argo submit --from workflowtemplate/prognostic-run \
        -p bucket=${BUCKET} \
        -p project=${PROJECT} \
        -p tag=${TAG} \
        -p config="$(< prognostic-config.yaml)" \
        -p segment-count=$SEGMENTS \
        -p memory="20Gi" \
        -p cpu="24" \
        -p online-diags-flags="--verification  1yr_pire_postspinup --n-jobs 5" \
        --name "${NAME}" \
        --labels "project=${PROJECT},experiment=${EXPERIMENT},trial=${TRIAL}"
done