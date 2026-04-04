import logging
from typing import Optional

from data.scraper import get_round_matches, get_rounds_unique_tournament
from processing import process_match_data
from data.mongo import serialize_document, insert_bulk

logger = logging.getLogger(__name__)


def maclari_al(
    tournament_id: Optional[int] = None,
    season_id: Optional[int] = None,
    week: Optional[int] = None,
    by_date: Optional[bool] = None,
    since_timestamp: Optional[int] = None,
):
    """Belirli bir lig, sezon ve haftadaki maçları getirir."""
    if by_date:
        if since_timestamp:
            data = get_rounds_unique_tournament(tournament_id, season_id)
            return [
                m for m in data["events"]
                if m.get("startTimestamp", 0) > since_timestamp
            ]
        return get_rounds_unique_tournament(tournament_id, season_id)
    return get_round_matches(tournament_id, season_id, week)


def mac_verisini_isle(
    match,
    insert_to_mongo: bool = False,
    collection_name: Optional[str] = None,
):
    """Tek bir maçın tüm verilerini işler ve uygun formata dönüştürür."""
    processed = process_match_data(match)

    if insert_to_mongo:
        if collection_name:
            data_list = processed if isinstance(processed, list) else [processed]
            result = insert_bulk(collection_name, data_list)
            logger.info(f"MongoDB insertion result: {result}")
        else:
            logger.warning(
                "insert_to_mongo is True but collection_name is None. Skipping MongoDB insertion."
            )
        return serialize_document(processed)

    return processed
