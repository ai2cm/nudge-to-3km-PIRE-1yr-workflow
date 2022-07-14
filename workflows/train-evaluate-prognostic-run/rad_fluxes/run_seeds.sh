#!/bin/bash

set -e



TMP_CONFIG=tmp-config.yml
TRIAL="rad-flux"

for i in {0..1}
do
    cp  training-config.yaml $TMP_CONFIG
    sed -i "s/^    random_seed: .*$/    random_seed: $i/" $TMP_CONFIG

    TAG=${EXPERIMENT}-${TRIAL}-seed-$i  # required
    NAME=$TAG  # required
    
    argo delete $NAME
    sleep 5

    argo submit --from workflowtemplate/train-diags-prog \
        -p bucket=${BUCKET} \
        -p project=${PROJECT} \
        -p tag=${TAG} \
        -p training-configs="$( yq . $TMP_CONFIG )" \
        -p training-data-config="$( yq . train-data.yaml )" \
        -p test-data-config="$( yq . test-data.yaml )" \
        -p validation-data-config="$( yq . val-data.yaml )" \
        -p training-flags="--cache.local_download_path train-data-download-dir" \
        -p prognostic-run-config="no_prog_run" \
        -p public-report-output=gs://vcm-ml-public/offline_ml_diags/$PROJECT/$TAG \
        -p segment-count="1" \
        -p memory-offline-diags="15Gi" \
        -p memory-training="27Gi" \
        -p online-diags-flags="--verification  1yr_pire_postspinup --n-jobs 5" \
        -p wandb-project="n2pire" \
        -p wandb-group=$EXPERIMENT \
        --name "${NAME}" \
        --labels "project=${PROJECT},experiment=${EXPERIMENT},trial=${TRIAL}"
    echo "argo get $NAME"
done