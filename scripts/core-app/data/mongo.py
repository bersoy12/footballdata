from typing import Any, Dict, List, Optional
# from mongodb_client import mongodb_client
import logging

logger = logging.getLogger(__name__)


def serialize_document(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


def insert_bulk(collection_name: str, data_list: List[Dict[str, Any]]) -> dict:
    result = mongodb_client.insert_bulk_raw_data(collection_name, data_list)
    logger.info(f"MongoDB insertion result: {result}")
    return {
        "success": result["successful"] > 0,
        "collection": collection_name,
        "successful": result["successful"],
        "failed": result["failed"],
    }


def get_raw_data(
    collection_name: str,
    query: Optional[dict] = None,
    projection: Optional[dict] = None,
    limit: int = 100,
) -> List[dict]:
    return mongodb_client.get_raw_data(collection_name, query, projection, limit)


def get_collections() -> List[str]:
    return mongodb_client.get_collections()
