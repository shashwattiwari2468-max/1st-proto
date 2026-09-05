from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
import xarray as xr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/ocean-grid")
def get_ocean_grid(depth_index: int = 0):
  ds = xr.open_dataset("sample_ocean_model.nc")
  temp_slice = ds["temperature"].isel(depth=depth_index).values

  lats = ds["lat"].values
  lons = ds["lon"].values

  grid_points = []
  for i, lat in enumerate(lats):
    for j, lon in enumerate(lons):
      val = temp_slice[i, j] if temp_slice.ndim == 2 else temp_slice[i]
      if not np.isnan(val):
        grid_points.append(
            {"lat": float(lat), "lon": float(lon), "temp": float(val)}
        )

  return {"points": grid_points}


@app.get("/api/insitu-observations")
def get_insitu_data():
  df = pd.read_csv("argo_floats.csv")
  return df.to_dict(orient="records")