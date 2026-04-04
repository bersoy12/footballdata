from typing import Optional, Set
from data.db import fetch_column


def gap_report(
    tournament_id: int,
    season_id: int,
    total_rounds: Optional[int] = None,
) -> dict:
    """
    Verilen turnuva ve sezon için veritabanındaki eksiklikleri raporlar.
    - Eksik round'lar
    - Statistic, incident, momentum eksik olan match_id'ler
    """
    all_match_ids = fetch_column("match_id", "match")
    all_tournament_ids = fetch_column("tournament_id", "match")
    all_season_ids = fetch_column("season_id", "match")
    all_rounds = fetch_column("round", "match")

    all_matches = [
        {"match_id": mid, "tournament_id": tid, "season_id": sid, "round": r}
        for mid, tid, sid, r in zip(
            all_match_ids, all_tournament_ids, all_season_ids, all_rounds
        )
    ]

    season_matches = [
        m for m in all_matches
        if m["tournament_id"] == tournament_id and m["season_id"] == season_id
    ]

    if not season_matches:
        return {
            "tournament_id": tournament_id,
            "season_id": season_id,
            "status": "no_data",
            "missing_rounds": list(range(1, (total_rounds or 1) + 1)),
            "fetched_rounds": [],
            "last_fetched_round": None,
            "matches_without_statistic": [],
            "matches_without_incident": [],
            "matches_without_momentum": [],
        }

    match_ids: Set[int] = {int(m["match_id"]) for m in season_matches}
    fetched_rounds = sorted(
        {int(m["round"]) for m in season_matches if m.get("round") is not None}
    )
    last_round = max(fetched_rounds) if fetched_rounds else None

    if total_rounds:
        missing_rounds = sorted(set(range(1, total_rounds + 1)) - set(fetched_rounds))
    elif fetched_rounds:
        full_range = set(range(min(fetched_rounds), max(fetched_rounds) + 1))
        missing_rounds = sorted(full_range - set(fetched_rounds))
    else:
        missing_rounds = []

    def missing_in_table(table_name: str) -> list:
        existing = fetch_column("match_id", table_name)
        existing_ids: Set[int] = set()
        for item in existing or []:
            val = item.get("match_id") if isinstance(item, dict) else item
            try:
                existing_ids.add(int(val))
            except (TypeError, ValueError):
                continue
        return sorted(match_ids - existing_ids)

    return {
        "tournament_id": tournament_id,
        "season_id": season_id,
        "fetched_rounds": fetched_rounds,
        "last_fetched_round": last_round,
        "missing_rounds": missing_rounds,
        "total_match_ids_in_db": len(match_ids),
        "matches_without_statistic": missing_in_table("statistic"),
        "matches_without_incident": missing_in_table("incident"),
        "matches_without_momentum": missing_in_table("momentum"),
    }
