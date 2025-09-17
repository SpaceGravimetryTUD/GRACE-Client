# grace_query/constants.py

"""This module defines project-level constants."""

CONFIG_PATH="./config.yml"
CONFIG_TMPLT = {"time": {"start": None, "end": None},
                "space": {"bbox": None, "polygon_str": None, "polygon_file": None, "polygon_crs": None},
                "export": {"format": None, "path": None, "strict_cf": None},
                "backend": {"url": None, "table": None, "srid": None}}

TABLE_ENVNAME="TABLE_NAME"
DB_ENVNAME="DATABASE_URL"

TIMECOL = "datetime"
TABLE_REQCOLS = ["id","datetime","latitude_A","longitude_A","postfit","up_combined"]

BBBOX_NARGS = 4
MAX_COORDS = 5
MAX_REPCOORDS = 2

SRID = 4326
POLYGON_CRS = f"EPSG:{SRID}"

CADENCE_SECONDS = 5
MISSING_THRESHOLD_PCT = 2.0

OUTPUT_DEFAULT = "netcdf"