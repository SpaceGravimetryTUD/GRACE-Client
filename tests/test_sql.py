import os
import pytest
from sqlalchemy import create_engine, text, inspect
from grace_query.sql import _get_allowed_columns

db_envname = "DATABASE_URL"
tbl_envname = "TABLE_NAME"
required_columns = ["id","datetime","latitude_A","longitude_A","postfit","up_combined","label","source"]

def engine():
    assert create_engine(os.getenv(db_envname)), "No database  found with the following URL: " + str(os.getenv(db_envname))
    return create_engine(os.getenv(db_envname))

def test_table_exists(engine=engine()):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert os.getenv(tbl_envname) in tables, "No table found in the database with the following name: " + str(os.getenv(tbl_envname))

def test_required_columns(engine=engine()):
    allowed_columns = _get_allowed_columns(engine)
    for col in required_columns:
        assert col in allowed_columns, "The following requested column could not be found back in the database table: " + col
