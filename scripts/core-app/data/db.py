import pandas as pd
from typing import Optional, List
from sql_alchemy import insert_table, fetch_data as _fetch_data
import logging

logger = logging.getLogger(__name__)


def insert_table_df(
    df: pd.DataFrame,
    table_name: str,
    on_conflict_columns: Optional[List[str]] = None,
    on_conflict_entire_columns: bool = False,
):
    """DataFrame'i belirtilen tabloya ekler."""
    if on_conflict_columns is None:
        on_conflict_columns = []
    return insert_table(
        df,
        table_name=table_name,
        on_conflict_columns=on_conflict_columns,
        on_conflict_entire_columns=on_conflict_entire_columns,
    )


def fetch_column(column_name: str, table_name: str):
    """Belirtilen tablodan tek bir sütun çeker."""
    return _fetch_data(column_name, table_name)
