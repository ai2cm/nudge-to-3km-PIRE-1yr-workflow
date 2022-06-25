"""
Save out a dataset to prescribe sea ice fraction along with the land sea mask.

However this is a bit of a pain because the c384 diags do not have this variable, need to take it from the coarsened restarts.
Saves at intervals of 1 week.

Since this is getting at seasonal variation try to just read a subset of weekly restarts, since the prescriber will handle time interpolation.
`hice` = sea ice thickness, rename to `sea_ice_thickness`
`fice` = ice fraction over open water, rename to `ice_fraction_over_open_water`
"""

import xarray as xr
import numpy as np
import fsspec
import intake
from vcm.catalog import catalog 
from vcm.safe import get_variables
from vcm.convenience import round_time
from dask.diagnostics import ProgressBar
import fv3viz
import cftime
import matplotlib.pyplot as plt
from datetime import timedelta

import vcm
from utils import cast_to_double, round_time_coord

OUTPUT_PATH = "gs://vcm-ml-intermediate/2021-08-03-PIRE-c48-diags-post-spinup/slmsk-seaice-reference.zarr"

restart_path = "gs://vcm-ml-intermediate/2021-08-06-PIRE-c48-restarts-post-spinup/{timestep}/{timestep}.sfc_data"
slmsk_data = intake.open_zarr("gs://vcm-ml-intermediate/2021-08-03-PIRE-c48-diags-post-spinup/sst-slmsk-time-centered.zarr").to_dask()

renamed = {"yaxis_1": "y", "xaxis_1": "x", "hice": "sea_ice_thickness", "fice": "ice_fraction_over_open_water"}
chunks = {"tile": 6, "time": 53, "x": 48, "y": 48}

slmsk = catalog["landseamask/c48"].read()
grid = catalog["grid/c48"].read()


times = [
    cftime.DatetimeJulian(2020, 1, 19) + timedelta(days=7) * i
    for i in range(53)
]


restarts = []

for t in times:
    restart = vcm.open_tiles(restart_path.format(timestep=vcm.encode_time(t)))[["hice", "fice"]]
    restart = restart.rename(renamed).squeeze().drop("Time")
    
    restart["land_sea_mask"] = slmsk_data["land_sea_mask"].interp(time=t)
    restarts.append(restart.assign_coords({"time": t}))

ice_restarts = xr.concat(restarts, dim="time").chunk(chunks).transpose("tile", "time", "y", "x")

with ProgressBar():
    ds = ice_restarts \
        .pipe(round_time_coord) \
        .pipe(cast_to_double)
    mapper = fsspec.get_mapper(OUTPUT_PATH)
    ds.to_zarr(mapper, consolidated=True)

print(f"Sea ice fraction and land sea mask prescriber data saved to {OUTPUT_PATH}.")