#!/bin/bash
name=$(date +%Ft%H%M%S)-$PROJECT-$EXPERIMENT
argo submit --from=workflowtemplate/prognostic-run-diags \
    --name $name \
    -p runs="$(< rundirs.json)" \
    -p recompute-diagnostics=false \
    -p flags="--verification  1yr_pire_postspinup --n-jobs 4" 

echo "report generated at: https://storage.googleapis.com/vcm-ml-public/argo/$name/index.html"
