# grace_query/export/__init__.py

"""This module contains handles the decision making step of exporting the queried data."""

# local imports
from .netcdf_cf import NetCDFWriter
from .csv_writer import CSVWriter
from .parquet_writer import ParquetWriter

def select_writer(fmt: str, options: dict):

    """Decide in which format data is exported. Currently supports netcdf, cdv and parquet"""

    fmt = (fmt or "netcdf").lower()
    if fmt == "netcdf": return NetCDFWriter(options)
    if fmt == "csv":    return CSVWriter(options)
    if fmt == "parquet":return ParquetWriter(options)
    raise ValueError(f"Unsupported format: {fmt}")