# tests/test_sql.py

"""This test checks that environment variables can identify the database and respective data table, and that the table column names match those expected by the code client"""


# standard libraries
import os

# third party imports
import pytest
from sqlalchemy import create_engine, text, inspect

# local imports
from grace_query import constants
from grace_query.sql import _get_allowed_columns

def engine():
    assert create_engine(os.getenv(constants.DB_ENVNAME)), "No database  found with the following URL: " + str(os.getenv(constants.DB_ENVNAME))
    return create_engine(os.getenv(constants.DB_ENVNAME))

def test_table_exists(engine=engine()):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert os.getenv(constants.TABLE_ENVNAME) in tables, "No table found in the database with the following name: " + str(os.getenv(constants.TABLE_ENVNAME))

def test_required_columns(engine=engine()):
    allowed_columns = _get_allowed_columns(engine)
    for col in constants.TABLE_REQCOLS:
        assert col in allowed_columns, "The following requested column could not be found back in the database table: " + col
