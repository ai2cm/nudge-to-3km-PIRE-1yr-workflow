#!/bin/bash

kubectl apply -k ../templates


argo submit --from workflowtemplate/save-netcdf-batches \
    -p config="$(< train.yaml)" \
    -p output="gs://$BUCKET/$PROJECT/data/tendencies/train" \
    -p memory="24Gi" \
    --name save-netcdf-training-tendencies



argo submit --from workflowtemplate/save-netcdf-batches \
    -p config="$(< validation.yaml)" \
    -p output="gs://$BUCKET/$PROJECT/data/tendencies/val" \
    -p memory="24Gi" \
    --name save-netcdf-validation-tendencies
