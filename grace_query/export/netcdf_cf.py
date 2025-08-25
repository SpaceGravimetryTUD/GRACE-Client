# grace_query/export/netcdf_cf.py
import pandas as pd, xarray as xr

class NetCDFWriter:
    def __init__(self, options: dict): self.opts = options or {}
    def write(self, df: pd.DataFrame, out_path: str) -> None:
        if df.empty: raise ValueError("Empty dataframe — nothing to write.")

        # time as dimension; lat/lon as coords (point track)
        t = pd.to_datetime(df["datetime"])
        ds = xr.Dataset(coords={"time": ("time", t.values)})
        if "latitude_A" in df:  ds["lat"] = ("time", df["latitude_A"].to_numpy()); ds["lat"].attrs.update({"standard_name":"latitude","units":"degrees_north"})
        if "longitude_A" in df: ds["lon"] = ("time", df["longitude_A"].to_numpy()); ds["lon"].attrs.update({"standard_name":"longitude","units":"degrees_east"})

        for col in df.columns:
            if col in ("datetime","latitude_A","longitude_A"): continue
            ds[col] = ("time", df[col].to_numpy())

        ds["time"].attrs.update({"standard_name":"time","axis":"T"})
        ds.attrs.update({
            "Conventions": "CF-1.8",
            "title": "GRACE query output",
            "history": "Created by grace-client",
            "source": "PostGIS/TimescaleDB"
        })

        # Optional compression/chunking
        encoding = None
        if self.opts.get("compression", True):
            encoding = {v: {"zlib": True, "complevel": 4} for v in ds.data_vars}

        if self.opts.get("strict_cf", False):
            # Minimal CF assertions — extend as needed
            for req in ("time","lat","lon"):
                if req not in ds:
                    raise ValueError(f"CF strict mode: missing coordinate '{req}'")

        ds.to_netcdf(out_path, encoding=encoding)