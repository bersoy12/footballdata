import json
import logging
from fastapi import APIRouter, Body, Query
from typing import Any, Dict, List, Optional
import pandas as pd

from data.db import insert_table_df, fetch_column
from data.mongo import insert_bulk, get_raw_data, get_collections

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/veritabanina-ekle")
def veritabanina_ekle_endpoint(
    table_name: str,
    data: List[Dict] = Body(...),
    on_conflict_columns: Optional[List[str]] = Query(default=[]),
):
    lst_of_data = [item for item in data if item is not None]
    df = pd.DataFrame(lst_of_data)
    logger.info(f"{len(df.index)} kayıt işlenecek.")
    return insert_table_df(df, table_name=table_name, on_conflict_columns=on_conflict_columns)


@router.get("/veritabanindan-cek")
def veritabanindan_cek_endpoint(table_name: str, column_name: str):
    return fetch_column(column_name, table_name)


@router.post("/mongodb/insert-raw-data")
def mongodb_insert_raw_data_endpoint(
    collection_name: str,
    data_list: List[Dict[str, Any]] = Body(...),
):
    """Birden fazla ham JSON verisini MongoDB'ye toplu olarak ekler."""
    return insert_bulk(collection_name, data_list)


@router.get("/mongodb/raw-data")
def mongodb_get_raw_data_endpoint(
    collection_name: str,
    query: Optional[str] = Query(default=None, description="MongoDB query filter as JSON string"),
    projection: Optional[str] = Query(default=None),
    limit: int = Query(description="Maximum number of documents to return"),
):
    """MongoDB'den ham veri çeker."""
    query_dict = None
    projection_dict = None

    if query:
        try:
            query_dict = json.loads(query)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON query string: {e}")
            return {"error": "Invalid JSON query string", "collection": collection_name, "count": 0, "data": []}

    if projection:
        try:
            projection_dict = json.loads(projection)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON projection string: {e}")
            return {"error": "Invalid JSON projection string", "collection": collection_name, "count": 0, "data": []}

    data = get_raw_data(collection_name, query_dict, projection_dict, limit)
    return {"collection": collection_name, "count": len(data), "data": data}


@router.get("/mongodb/collections")
def mongodb_get_collections_endpoint():
    """Veritabanındaki tüm koleksiyonları listeler."""
    return {"collections": get_collections()}