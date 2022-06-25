import xarray as xr
import numpy as np

from vcm.convenience import round_time


def set_missing_units_attr(ds: xr.Dataset) -> xr.Dataset:
    for var in ds:
        da = ds[var]
        if "units" not in da.attrs:
            da.attrs["units"] = "unspecified"
    return ds


def cast_to_double(ds: xr.Dataset) -> xr.Dataset:
    new_ds = {}
    for name in ds.data_vars:
        if ds[name].values.dtype != np.float64:
            new_ds[name] = (
                ds[name]
                .astype(np.float64, casting="same_kind")
                .assign_attrs(ds[name].attrs)
            )
        else:
            new_ds[name] = ds[name]
    return xr.Dataset(new_ds).assign_attrs(ds.attrs)


def round_time_coord(ds: xr.Dataset) -> xr.Dataset:
    return ds.assign_coords({"time": round_time(ds.coords["time"])})
