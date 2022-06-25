import xarray as xr
import numpy as np
import fsspec
import intake
from vcm.catalog import catalog 
from vcm.safe import get_variables
from vcm.convenience import round_time
from dask.diagnostics import ProgressBar

from datetime import timedelta

from utils import cast_to_double, round_time_coord


RENAME = {
    'grid_yt': 'y',
    'grid_xt': 'x',
}

INPUT_PATH = 'gs://vcm-ml-intermediate/2021-08-03-PIRE-c48-diags-post-spinup/pire_atmos_phys_3h_coarse.zarr'
OUTPUT_PATH = "gs://vcm-ml-intermediate/2021-08-03-PIRE-c48-diags-post-spinup/sst-slmsk-time-centered.zarr"


ds_orig = intake.open_zarr(INPUT_PATH).to_dask()
times_shifted = [t - timedelta(hours=1, minutes=30) for t in ds_orig.time.values]
ds_shifted = ds_orig.assign_coords({"time": times_shifted}).rename(RENAME)

# leave sea ice points too since land sea mask can change from sea to sea ice depending on time of year
ds_shifted["ocean_surface_temperature"] = ds_shifted["tsfc_coarse"]
ds_shifted["ocean_surface_temperature"].attrs["long name"] = "Surface temperature over sea and sea ice"

with ProgressBar():
    ds = ds_shifted[["ocean_surface_temperature"]] \
        .pipe(round_time_coord) \
        .pipe(cast_to_double)
    mapper = fsspec.get_mapper(OUTPUT_PATH)
    ds.to_zarr(mapper, consolidated=True)

print(f"Wrote prescribed sea surface temperatures to {OUTPUT_PATH}.")