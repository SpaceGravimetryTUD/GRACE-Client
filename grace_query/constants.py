"""This module defines project-level constants."""

TABLE_ENVNAME="TABLE_NAME"
DB_ENVNAME="DATABASE_URL"

TABLE_REQCOLS = ["id","datetime","latitude_A","longitude_A","postfit","up_combined"]

MAX_COORDS = 5
MAX_REPCOORDS = 2

CADENCE_SECONDS = 5
MISSING_THRESHOLD_PCT = 2.0