from fastapi import APIRouter, Query
from typing import Optional

from services.report_service import gap_report

router = APIRouter()


@router.get("/gap-report")
def gap_report_endpoint(
    tournament_id: int,
    season_id: int,
    total_rounds: Optional[int] = Query(
        default=None,
        description="Sezondaki toplam hafta sayısı (bilinmiyorsa boş bırakın)",
    ),
):
    """
    Verilen turnuva ve sezon için veritabanındaki eksiklikleri raporlar.
    - Eksik round'lar
    - Statistic, incident, momentum eksik olan match_id'ler
    """
    return gap_report(tournament_id, season_id, total_rounds)