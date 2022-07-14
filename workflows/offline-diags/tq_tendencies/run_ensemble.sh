#!/bin/bash

set -e


TRIAL="tq-tendencies"
TMP_CONFIG=tmp-config.yml

cp  training-config.yaml $TMP_CONFIG

TAG=no-taper-${TRIAL}-ensemble  # required
NAME=$TAG-offline-diags # required

argo delete $NAME
sleep 5

argo submit --from workflowtemplate/offline-diags \
    -p ml-model="gs://vcm-ml-experiments/n2f-pire-stable-ml/2022-05-17/tapering-effect-mae-no-taper-ensemble/trained_models/tq_tendencies" \
    -p training_config="$( yq . $TMP_CONFIG )" \
    -p training_data_config="$( yq . train-data.yaml )" \
    -p test_data_config="$( yq . test-data.yaml )" \
    -p offline-diags-output="gs://vcm-ml-experiments/n2f-pire-stable-ml/2022-05-17/tapering-effect-mae-no-taper-ensemble/offline_diags/tq_tendencies" \
    -p report-output=gs://vcm-ml-public/offline_ml_diags/$PROJECT/$TAG \
    -p memory="15Gi" \
    --name "${NAME}" \
    --labels "project=${PROJECT},experiment=${EXPERIMENT},trial=${TRIAL}"
echo "argo get $NAME"
