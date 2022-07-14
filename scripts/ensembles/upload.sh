#!/bin/bash

gsutil cp -r \
    radiative_fluxes_ensemble \
    gs://vcm-ml-experiments/n2f-pire-stable-ml/2022-07-06/decrease-rad-lr-rad-flux-ensemble/trained_models/radiative_fluxes

gsutil cp -r \
    tq_tendencies_ensemble \
    gs://vcm-ml-experiments/n2f-pire-stable-ml/2022-05-17/tapering-effect-mae-no-taper-ensemble/trained_models/tq_tendencies
