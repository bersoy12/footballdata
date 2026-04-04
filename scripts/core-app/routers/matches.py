import time
import logging
from fastapi import APIRouter, Body, Query
from typing import Optional, List

from services.match_service import maclari_al, mac_verisini_isle

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/maclari-al")
def maclari_al_endpoint(
    tournament_id: int = None,
    season_id: int = None,
    week: Optional[int] = None,
    start_week: Optional[int] = None,
    end_week: Optional[int] = None,
    by_date: Optional[bool] = None,
    since_timestamp: Optional[int] = Query(
        default=None,
        description="Current timestamp {}".format(int(time.time())),
    ),
):
    """Belirtilen hafta ya da haftalarda oynanan tüm maçları çeker."""
    if by_date:
        logger.info("Günlük olarak maçlar alınıyor...")
        return maclari_al(tournament_id, season_id, by_date=by_date, since_timestamp=since_timestamp)

    if start_week:
        matches = []
        for w in range(start_week, (end_week or start_week) + 1):
            try:
                logger.info(f"Hafta {w} maçları alınıyor...")
                matches += maclari_al(tournament_id, season_id, w)
            except Exception:
                continue
        return matches

    return maclari_al(tournament_id, season_id, week)


@router.post("/mac-verisini-isle")
def mac_verisini_isle_endpoint(
    matches: List = Body(...),
    insert_to_mongo: bool = Query(default=False),
    collection_name: str = None,
):
    return [
        mac_verisini_isle(match, insert_to_mongo=insert_to_mongo, collection_name=collection_name)
        for match in matches
    ]