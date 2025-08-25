# grace_query/export/__init__.py
from .netcdf_cf import NetCDFWriter
from .csv_writer import CSVWriter
from .parquet_writer import ParquetWriter

def select_writer(fmt: str, options: dict):
    fmt = (fmt or "netcdf").lower()
    if fmt == "netcdf": return NetCDFWriter(options)
    if fmt == "csv":    return CSVWriter(options)
    if fmt == "parquet":return ParquetWriter(options)
    raise ValueError(f"Unsupported format: {fmt}")