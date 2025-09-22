# grace_query/constants.py

"""This module defines project-level constants."""

# ./config.yml related constants
CONFIG_PATH="./config.yml"
CONFIG_TMPLT = {"time": {"start": None, "end": None},
                "space": {"bbox": None, "polygon_str": None, "polygon_file": None, "polygon_crs": None},
                "export": {"format": None, "path": None, "strict_cf": None},
                "backend": {"url": None, "table": None, "srid": None}}

# ./.env related constants
TABLE_ENVNAME="TABLE_NAME"
DB_ENVNAME="DATABASE_URL"

# SQL Table columns related constants
DATETIMECOL = "datetime"
LONCOL = "longitude_A"
LATCOL = "latitude_A"
TABLE_REQCOLS = ["id","datetime","latitude_A","longitude_A","postfit","up_combined"]

# polygon configuration related constants
BBBOX_NARGS = 4
MAX_COORDS = 5
MAX_REPCOORDS = 2
SRID = 4326
POLYGON_CRS = f"EPSG:{SRID}"

# problematic month related constants
CADENCE_SECONDS = 5
MISSING_THRESHOLD_PCT = 2.0

# export related constants
OUTPUT_DEFAULT = "netcdf"
OUTPUT_EXT = "nc"