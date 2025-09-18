# grace_query/sql.py

"""This module translates the querying configurations into SQL statement returns the data query."""

# standard libraries
import os

# third party imports
import pandas as pd
from sqlalchemy import create_engine, text, inspect

# local imports
from grace_query import constants


def _get_allowed_columns(engine) -> list:
    "Get collumn names from table stored in database and take those as the allowed collumn names to be covered by querying settings"

    try:
        inspector = inspect(engine)
        allowed = [col["name"] for col in inspector.get_columns(os.getenv(constants.TABLE_ENVNAME))]
    except:
        with engine.connect() as conn:
            allowed = list(pd.read_sql_query(text(f"""SELECT * FROM {os.getenv(constants.TABLE_ENVNAME)}"""), conn).columns)
    return allowed

def _columns_clause(requested, allowed):
    "Make list of columns to be covered by data querying, in addition to the columns that have to be covered, listed in constants.TABLE_REQCOLS"

    pick = constants.TABLE_REQCOLS

    for c in requested:
        if c in allowed and c not in pick:
            pick.append(c)
            
    return ", ".join(f'"{c}"' if c != constants.TIMECOL else constants.TIMECOL for c in pick)

def run_query(db_url, table, start, end, space, columns):
    "Make a SQL statement covering all the querying settings and run query based on it."

    if not db_url or not table:
        raise ValueError("Database URL and table name are required (from flags, YAML or env).")
    engine = create_engine(db_url)

    allowed_columns = _get_allowed_columns(engine)

    # Whitelist known columns to avoid injection via column names
    cols = _columns_clause(columns or [], allowed_columns)

    time_pred = []
    params = {}
    if start: time_pred.append(str(constants.TIMECOL + " >= :start")); params["start"] = pd.to_datetime(start)
    if end:   time_pred.append(str(constants.TIMECOL + " <  :end"));   params["end"]   = pd.to_datetime(end)

    space_pred = []
    if space and "wkt" in space:
        space_pred.append(f"""
          ST_Contains(
            ST_GeomFromText(:wkt, :srid),
            ST_SetSRID(ST_MakePoint("{(str(constants.LONCOL))}", "{(str(constants.LATCOL))}"), :srid)
          )
        """)
        params["wkt"] = space["wkt"]
        params["srid"] = space["srid"]

    predicates = " AND ".join([*time_pred, *space_pred]) or "TRUE"
    query = text(f'SELECT {cols} FROM "{table}" WHERE {predicates} ORDER BY {constants.TIMECOL} ASC')

    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df