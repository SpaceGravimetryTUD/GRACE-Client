# grace_query/export/parquet_writer.py

"""This module contains the class to export data in parquet format."""

class ParquetWriter:
    def __init__(self, options: dict): pass
    def write(self, df, out_path): df.to_parquet(out_path, index=False)