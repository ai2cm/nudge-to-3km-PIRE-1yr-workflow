import cftime
import xarray as xr
import pandas as pd


labels = ["JFM", "AMJ", "JAS", "OND"]

def seasonal_avg(ds):
    seasonal_ = []
    start_year = ds.time.values[0].year
    seasons = [
        slice(cftime.DatetimeJulian(start_year,1,1), cftime.DatetimeJulian(start_year,4,1)),
        slice(cftime.DatetimeJulian(start_year,4,1), cftime.DatetimeJulian(start_year,7,1)),
        slice(cftime.DatetimeJulian(start_year,7,1), cftime.DatetimeJulian(start_year,10,1)),
        slice(cftime.DatetimeJulian(start_year,10,1), cftime.DatetimeJulian(start_year + 1, 1,1)),
    ]    
    for season in seasons:
        seasonal_.append(ds.sel(time=season).mean("time"))
    return xr.concat(seasonal_, dim=pd.Index([str(v) for v in labels], name="season")).load()