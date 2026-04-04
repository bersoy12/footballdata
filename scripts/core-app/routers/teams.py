from fastapi import APIRouter, Query
from typing import Optional

from services.teams_service import takimlari_getir

router = APIRouter()

@router.get("/takimlari-getir")
def takimlari_getir_endpoint(
    unique_tournament_id: int,
    season_id: int
):
    return takimlari_getir(unique_tournament_id, season_id)