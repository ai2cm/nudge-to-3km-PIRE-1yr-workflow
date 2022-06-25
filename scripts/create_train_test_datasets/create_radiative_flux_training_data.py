import intake
import xarray as xr
from dask.diagnostics import ProgressBar
import dask
import fsspec
import os

PROJECT = os.environ["PROJECT"]

PRESCRIBED_DATA_PATH = 'gs://vcm-ml-intermediate/2021-08-03-PIRE-c48-diags-post-spinup/fine-res-surface-radiative-fluxes-transm-precip-time-centered.zarr'
NUDGED_STATE_PATH = "gs://vcm-ml-experiments/n2f-pire-sfc-updates/2022-01-21/nudged-run/fv3gfs_run/state_after_timestep.zarr"
OUTPUT_PATH = f"gs://vcm-ml-experiments/{PROJECT}/data/rad-train-test-data-time-centered-with-toa.zarr"

def clear_chunks_encoding(ds: xr.Dataset):
    for variable in ds:
        if "chunks" in ds[variable].encoding:
            del ds[variable].encoding["chunks"]
    return ds


def chunk(ds: xr.Dataset, dim= "time", size: str = "256Mi"):
    """Chunk a dataset such that chunks have a certain data size"""
    chunks = {dim: "auto", "tile": 6}
    ds = clear_chunks_encoding(ds)
    with dask.config.set({"array.chunk-size": size}):
        return ds.chunk(chunks)

state = intake.open_zarr(NUDGED_STATE_PATH).to_dask()
reference = intake.open_zarr(PRESCRIBED_DATA_PATH).to_dask()

overlap_times = sorted(list(set(state.time.values).intersection(reference.time.values)))
state_vars = [
    "surface_diffused_shortwave_albedo",
    "longitude",
    "latitude",
    "surface_geopotential",
    "air_temperature",
    "specific_humidity",
    "land_sea_mask",
    "pressure_thickness_of_atmospheric_layer",
    "surface_geopotential",
]
merged = xr.merge([
    state[state_vars].sel(time=overlap_times),
    reference.sel(time=overlap_times),]
)
with ProgressBar():
    mapper = fsspec.get_mapper(OUTPUT_PATH)
    merged = clear_chunks_encoding(merged).unify_chunks()
    merged.to_zarr(mapper, consolidated=True, mode="w")
    
