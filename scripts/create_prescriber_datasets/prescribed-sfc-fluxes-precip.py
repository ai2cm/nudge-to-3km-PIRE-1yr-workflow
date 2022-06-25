"""
PIRE surface diagnostics are saved as time averages over a window, 
but with the marked time as being the *end* of that interval, not the middle.
Since the PIRE data is averaged over a 3 hour window, the correction is to 
reassign the time coordinate by subtracting off 1.5 hr.
"""

from datetime import timedelta
import xarray as xr
import numpy as np
import fsspec
import intake
from vcm.catalog import catalog
from vcm.safe import get_variables
from vcm.convenience import round_time
from dask.diagnostics import ProgressBar

from utils import set_missing_units_attr, round_time_coord, cast_to_double


VARIABLES = ['DSWRFsfc_coarse', 'DLWRFsfc_coarse', 'USWRFsfc_coarse', 'PRATEsfc_coarse', 'DSWRFtoa_coarse']
RENAME = {
    'grid_yt': 'y',
    'grid_xt': 'x',
    'DSWRFsfc_coarse': 'override_for_time_adjusted_total_sky_downward_shortwave_flux_at_surface',
    'DLWRFsfc_coarse': 'override_for_time_adjusted_total_sky_downward_longwave_flux_at_surface',
    'NSWRFsfc_coarse': 'override_for_time_adjusted_total_sky_net_shortwave_flux_at_surface',
    'DSWRFtoa_coarse': 'total_sky_downward_shortwave_flux_at_top_of_atmosphere',
}

INPUT_PATH = 'gs://vcm-ml-intermediate/2021-08-03-PIRE-c48-diags-post-spinup/pire_atmos_phys_3h_coarse.zarr'
OUTPUT_PATH = 'gs://vcm-ml-intermediate/2021-08-03-PIRE-c48-diags-post-spinup/fine-res-surface-radiative-fluxes-transm-precip-time-centered.zarr'

timestep_seconds = 900.0
m_per_mm = 1/1000

def add_total_precipitation(ds: xr.Dataset) -> xr.Dataset:
    total_precipitation = ds['PRATEsfc_coarse']*m_per_mm*timestep_seconds
    total_precipitation = total_precipitation.assign_attrs({
        "long_name": "precipitation increment to land surface",
        "units": "m",
    })
    ds['total_precipitation'] = total_precipitation
    return ds.drop_vars('PRATEsfc_coarse')

def add_net_shortwave(ds: xr.Dataset) -> xr.Dataset:
    net_shortwave = ds["DSWRFsfc_coarse"] - ds["USWRFsfc_coarse"]
    net_shortwave = net_shortwave.assign_attrs(
        {
            "long_name": "net shortwave radiative flux at surface (downward)",
            "units": "W/m^2",
        }
    )
    ds["NSWRFsfc_coarse"] = net_shortwave
    return ds.drop_vars("USWRFsfc_coarse")

def add_transmissivity(ds):
    ds["shortwave_transmissivity_of_atmospheric_column"] = xr.where(
        ds['DSWRFtoa_coarse'] > 0.,
        ds['DSWRFsfc_coarse'] / ds['DSWRFtoa_coarse'],
        0.
    )
    return ds

with ProgressBar():
    ds = (
        get_variables(intake.open_zarr(INPUT_PATH).to_dask(), VARIABLES)
        .pipe(set_missing_units_attr)
        .pipe(add_net_shortwave)
        .pipe(add_total_precipitation)
        .pipe(add_transmissivity)
        .pipe(cast_to_double)
        .pipe(round_time_coord)
        .rename(RENAME)
    )

    times_shifted = [t - timedelta(hours=1, minutes=30) for t in ds.time.values]
    ds_shifted = ds.assign_coords({"time": times_shifted})

    mapper = fsspec.get_mapper(OUTPUT_PATH)
    ds_shifted.to_zarr(mapper, consolidated=True)