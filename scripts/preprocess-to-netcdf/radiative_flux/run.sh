#!/bin/bash

kubectl apply -k ../templates


argo submit --from workflowtemplate/save-netcdf-batches \
    -p config="$(< train.yaml)" \
    -p output="gs://$BUCKET/$PROJECT/data/rad_fluxes_train" \
    -p memory="24Gi" \
    --name save-netcdf-training-rad



argo submit --from workflowtemplate/save-netcdf-batches \
    -p config="$(< validation.yaml)" \
    -p output="gs://$BUCKET/$PROJECT/data/rad_fluxes_val" \
    -p memory="24Gi" \
    --name save-netcdf-validation-rad
