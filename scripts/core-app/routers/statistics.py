from fastapi import APIRouter, Body, Query
from typing import List
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from itertools import chain

from services.stats_service import (
    mac_istatistiklerini_isle,
    mac_grafiklerini_isle,
    mac_olaylarini_isle,
    takim_istatistiklerini_getir,
)


router = APIRouter()


class PayloadType(str, Enum):
    statistics = "İstatistik"
    graphs = "Momentum Grafiği"
    events = "Olaylar"


@router.post("/veri-topla")
def istatistikleri_al_endpoint(
    match_ids: List[int] = Body(...),
    payload: PayloadType = Query(..., embed=True),
    insert_simultaneously: bool = False,
    insert_to_mongo: bool = False,
):
    """Birden fazla maç için istatistikleri/grafikleri paralel olarak işler."""
    fn_map = {
        PayloadType.statistics: mac_istatistiklerini_isle,
        PayloadType.graphs: mac_grafiklerini_isle,
        PayloadType.events: mac_olaylarini_isle,
    }

    fn = fn_map.get(payload)
    if fn is None:
        return None

    with ThreadPoolExecutor(max_workers=1) as executor:
        results = list(
            executor.map(
                lambda mid: fn(mid, insert_simultaneously, insert_to_mongo),
                match_ids,
            )
        )

    list(chain.from_iterable(results))
    return None


@router.get("/takim-istatistiklerini-getir")
def takim_istatistiklerini_getir_endpoint(
    team_id: int,
    unique_tournament_id: int,
    season_id: int,
    insert_to_db: bool = False,
):
    return takim_istatistiklerini_getir(team_id, unique_tournament_id, season_id, insert_to_db)