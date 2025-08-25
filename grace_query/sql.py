# grace_client/sql.py
import pandas as pd
from sqlalchemy import create_engine, text

def _columns_clause(requested_cols, allowed):
    pick = [c for c in requested_cols if c in allowed]
    if not pick: 
        pick = ["id","datetime","latitude_A","longitude_A","postfit","up_combined"]
    return ", ".join(f'"{c}"' if c != "datetime" else "datetime" for c in pick)

def run_query(db_url, table, start, end, space, columns):
    if not db_url or not table:
        raise ValueError("Database URL and table name are required (from flags, YAML or env).")
    engine = create_engine(db_url)

    # Whitelist known columns to avoid injection via column names
    allowed = {"id","datetime","latitude_A","longitude_A","postfit","up_combined","altitude_A","up_local","up_common","up_global"}
    cols = _columns_clause(columns or [], allowed)

    time_pred = []
    params = {}
    if start: time_pred.append("datetime >= :start"); params["start"] = pd.to_datetime(start)
    if end:   time_pred.append("datetime <  :end");   params["end"]   = pd.to_datetime(end)

    space_pred = []
    if space and "wkt" in space:
        space_pred.append("""
          ST_Contains(
            ST_GeomFromText(:wkt, :srid),
            ST_SetSRID(ST_MakePoint("longitude_A","latitude_A"), :srid)
          )
        """)
        params["wkt"] = space["wkt"]
        params["srid"] = space["srid"]

    predicates = " AND ".join([*time_pred, *space_pred]) or "TRUE"
    query = text(f'SELECT {cols} FROM "{table}" WHERE {predicates} ORDER BY datetime ASC')

    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df