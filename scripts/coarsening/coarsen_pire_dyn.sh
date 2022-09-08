#!/bin/bash

python /home/AnnaK/fv3net/workflows/coarsen_c384_diagnostics/coarsen_c384_diagnostics.py \
    gs://vcm-ml-raw-flexible-retention/2021-07-19-PIRE/C3072-to-C384-res-diagnostics/pire_atmos_dyn_plev_coarse_3h.zarr \
    /home/AnnaK/explore/annak/2021-07-30-PIRE-nudging-data/coarsen-pire-c384-dyn-plev.yml \
    gs://vcm-ml-intermediate/2021-09-22-PIRE-c48-dycore-post-spinup/pire_atmos_dyn_plev_coarse_3h.zarr


python /home/AnnaK/fv3net/workflows/coarsen_c384_diagnostics/coarsen_c384_diagnostics.py \
    gs://vcm-ml-raw-flexible-retention/2021-07-19-PIRE/C3072-to-C384-res-diagnostics/pire_atmos_dyn_3h_coarse_inst.zarr \
    /home/AnnaK/explore/annak/2021-07-30-PIRE-nudging-data/coarsen-pire-c384-dyn.yml \
    gs://vcm-ml-intermediate/2021-09-22-PIRE-c48-dycore-post-spinup/pire_atmos_dyn_3h_coarse_inst.zarr