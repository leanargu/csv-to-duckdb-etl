# pipeline/persist.py

import duckdb
import pandas as pd


def save_to_duckdb(df: pd.DataFrame, table_name: str, db_path: str) -> None:
    """
    Save a DataFrame as a table in a DuckDB file.

    Args:
        df (pd.DataFrame): The data to persist
        table_name (str): Name of the table
        db_path (str): Path to the .duckdb file
    """
    try:
        con = duckdb.connect(db_path)
        con.execute(f"DROP TABLE IF EXISTS {table_name}")
        con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
        print(f"[Persist] Saved DataFrame to DuckDB table '{table_name}' in '{db_path}'")
    except Exception as e:
        print(f"[Persist] Error saving to DuckDB: {e}")
        raise