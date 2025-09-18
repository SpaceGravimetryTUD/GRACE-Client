# grace_query/export/csv_writer.py

"""This module contains the class to export data in csv format."""

class CSVWriter:
    def __init__(self, options: dict): pass
    def write(self, df, out_path): df.to_csv(out_path, index=False)