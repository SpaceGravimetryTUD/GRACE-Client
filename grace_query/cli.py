# grace_query/cli.py
import argparse, os, sys
from .config import getenv, load_config, merge_cli_over_config
from .polygons import parse_space  # returns dict with {'wkt': 'POLYGON(...)', 'srid': 4326} or None
from .sql import run_query         # returns pandas DataFrame
from .problematic import diagnose, ProblematicConfig
from .export import select_writer  # returns a writer with .write(df, out_path)

def main():
    parser = argparse.ArgumentParser(prog="grace query", description="GRACE CLI Query Tool")
    subparsers = parser.add_subparsers(dest="command")

    query_parser = subparsers.add_parser("query", help="Query KBR Gravimetry Data within polygon and time bounds.")
    query_parser.add_argument("--config")
    query_parser.add_argument("--start-time", type=str, help="Start time (e.g. '2017-01-01T00:00:00')")
    query_parser.add_argument("--end-time", type=str, help="End time (e.g. '2017-02-01T00:00:00')")
    query_parser.add_argument("--bbox", nargs=4, type=float)
    query_parser.add_argument("--polygon-str", type=str, help="Polygon coordinates as 'lon1 lat1,lon2 lat2,...,lonN latN'")
    query_parser.add_argument("--polygon-file")
    query_parser.add_argument("--polygon-crs", default="EPSG:4326")
    query_parser.add_argument("--params")
    query_parser.add_argument("--out-format", type=str, default="netcdf", choices=["netcdf","csv","parquet"], help="Output format (csv or netcdf)")
    query_parser.add_argument("--out-path")
    query_parser.add_argument("--problematic-report")
    query_parser.add_argument("--strict-cf", action="store_true")
    query_parser.add_argument("--db-url")                # optional override
    query_parser.add_argument("--table")                 # optional override

    args = parser.parse_args()

    cfg = load_config(args.config)
    cfg = merge_cli_over_config(cfg, args)    # normalize, parse dates/params

    space = parse_space(
        bbox=cfg.space.bbox, 
        polygon_str=cfg.space.polygon_str,
        polygon_file=cfg.space.polygon_file,
        polygon_crs=cfg.space.polygon_crs,
        target_srid=cfg.backend.srid
    )
    df = run_query(
        db_url=cfg.backend.url or getenv("DATABASE_URL"),
        table=cfg.backend.table or getenv("TABLE_NAME"),
        start=cfg.time.start, end=cfg.time.end,
        space=space, columns=cfg.columns
    )

    
    # Problematic months (optional)
    if cfg.problematic:
        rep = diagnose(df, time_col="datetime", cfg=ProblematicConfig(
            cadence_seconds=cfg.problematic.cadence_seconds,
            missing_threshold_pct=cfg.problematic.missing_threshold_pct
        ))
        if cfg.problematic.report_path:
            rep.to_json(cfg.problematic.report_path, orient="records", indent=2)
    

    if (cfg.time.start is not None or cfg.time.end is not None) and space is None:
        print("\n--- Time Filter Only ---")
    elif space is not None and cfg.time.start is None and cfg.time.end is None:
        print("\n--- Space Filter Only (Polygon) ---")
    elif space is not None and (cfg.time.start is not None or cfg.time.end is not None):
        print("\n--- Time + Space Filter (Combined) ---")
    else:
        raise ValueError("Unexpected query arguments!")
    
    print(df)

    # Export
    out_path = cfg.export.out
    writer = select_writer(cfg.export.format, cfg.export.options | {"strict_cf": cfg.export.strict_cf})
    writer.write(df, out_path)
    print(f"✅ Wrote {out_path}")