#!/bin/bash

set -e


TRIAL="rad-flux"
TMP_CONFIG=tmp-config.yml

for i in {0..3}
do
    cp  training-config.yaml $TMP_CONFIG
    sed -i "s/^    random_seed: .*$/    random_seed: $i/" $TMP_CONFIG

    TAG=${EXPERIMENT}-${TRIAL}-seed-$i  # required
    NAME=$TAG-offline-diags # required
    
    #argo delete $NAME
    #sleep 5

    argo submit --from workflowtemplate/offline-diags \
        -p ml-model="gs://vcm-ml-experiments/n2f-pire-stable-ml/2022-07-06/decrease-rad-lr-rad-flux-seed-$i/trained_models/radiative_fluxes/" \
        -p training_config="$( yq . $TMP_CONFIG )" \
        -p training_data_config="$( yq . train-data.yaml )" \
        -p test_data_config="$( yq . test-data.yaml )" \
        -p offline-diags-output="gs://vcm-ml-experiments/n2f-pire-stable-ml/2022-07-06/decrease-rad-lr-rad-flux-seed-$i/offline_diags/radiative_fluxes/" \
        -p report-output=gs://vcm-ml-public/offline_ml_diags/$PROJECT/$TAG \
        -p memory="15Gi" \
        --name "${NAME}" \
        --labels "project=${PROJECT},experiment=${EXPERIMENT},trial=${TRIAL}"
    echo "argo get $NAME"
done