from fastapi import APIRouter, Body
from typing import Optional, List

from services.pipeline_service import run_pipeline

router = APIRouter()


@router.post("/pipeline/run")
def pipeline_run_endpoint(
    tournament_id: Optional[int] = Body(None),
    season_ids: Optional[List[int]] = Body(None),
    by_date: bool = Body(True),
):
    """
    Belirtilen turnuva ve sezonlar için tam pipeline'ı çalıştırır:
    maç çek → işle → DB'ye yaz → istatistik/grafik/olay topla.
    """
    if not tournament_id:
        return {"error": "tournament_id is required"}
    return run_pipeline(tournament_id, season_ids, by_date)