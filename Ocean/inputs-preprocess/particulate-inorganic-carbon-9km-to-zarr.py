import xarray as xr
import numpy as np
from glob import glob
from tqdm import tqdm
from datetime import datetime
import os

pathIn = f"~/data/ocean/source/particulate_inorganic_carbon/"
pathIn = os.path.expanduser(pathIn)

files = glob(f"{pathIn}/*.nc")
files.sort()

for file in tqdm(files):
    filename = file.split("/")[-1].replace(".nc",".zarr")
    if not os.path.exists(f"{pathIn}{filename}"):
        date = np.datetime64(datetime.strptime(filename.split("-")[-2], '%Y%m'))
        ds = xr.open_dataset(file)
        ds = ds.astype("float32")
        if ("latitude" in ds.variables) and ("longitude" in ds.variables):
            ds = ds.drop(["latitude","longitude"])
        ds = ds.expand_dims(dict(time=[date]))
        ds['time'] = ds.time.astype('datetime64[M]')
        ds = ds.chunk(dict(time=1,lon=256,lat=256))
        ds.to_zarr(f"{pathIn}{filename}")
