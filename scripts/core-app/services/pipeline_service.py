import logging
import pandas as pd
from typing import Optional, List, Union, Set

from services.match_service import maclari_al, mac_verisini_isle
from services.stats_service import (
    mac_istatistiklerini_isle,
    mac_grafiklerini_isle,
    mac_olaylarini_isle,
)
from data.db import insert_table_df, fetch_column

logger = logging.getLogger(__name__)

PAYLOAD_TABLE_MAP = {
    "İstatistik": "statistic",
    "Momentum Grafiği": "momentum",
    "Olaylar": "incident",
}


def _extract_match_ids(resp: Union[dict, list]) -> List[int]:
    """Nested JSON yapısından tüm match_id değerlerini çeker."""
    ids = []
    if isinstance(resp, dict):
        for k, v in resp.items():
            if k == "match_id" and (
                isinstance(v, int) or (isinstance(v, str) and v.isdigit())
            ):
                ids.append(int(v))
            else:
                ids.extend(_extract_match_ids(v))
    elif isinstance(resp, list):
        for item in resp:
            ids.extend(_extract_match_ids(item))
    return ids


def _fetch_existing_ids(table_name: str) -> Set[int]:
    """Hedef tablodan mevcut match_id setini döner."""
    existing_ids: Set[int] = set()
    try:
        existing = fetch_column("match_id", table_name)
    except Exception:
        return existing_ids

    for item in existing or []:
        val = item.get("match_id") if isinstance(item, dict) else item
        try:
            existing_ids.add(int(val))
        except (TypeError, ValueError):
            continue
    return existing_ids


def _run_payload(
    payload: str,
    match_ids: List[int],
    season_id: Optional[int],
    errors: List[str],
):
    if not match_ids:
        logger.info(f"No match_ids to process for payload {payload} (season {season_id}).")
        return

    target_table = PAYLOAD_TABLE_MAP[payload]
    existing_ids = _fetch_existing_ids(target_table)
    to_process = [mid for mid in match_ids if mid not in existing_ids]

    if not to_process:
        logger.info(
            f"All match_ids already present for table {target_table}; "
            f"skipping payload {payload} for season {season_id}."
        )
        return

    fn_map = {
        "İstatistik": mac_istatistiklerini_isle,
        "Momentum Grafiği": mac_grafiklerini_isle,
        "Olaylar": mac_olaylarini_isle,
    }

    try:
        for match_id in to_process:
            fn_map[payload](match_id, insert_simultaneously=True, insert_to_mongo=False)
    except Exception as e:
        logger.error(f"Error while running payload {payload} for season {season_id}: {e}")
        errors.append(str(e))


def run_pipeline(
    tournament_id: int,
    season_ids: Optional[List[int]] = None,
    by_date: bool = True,
) -> dict:
    """
    Tam pipeline: maç çek → işle → DB'ye yaz → istatistik/grafik/olay topla.
    """
    summary = {"tournament_id": tournament_id, "seasons": {}, "errors": []}

    if not season_ids:
        season_ids = [None]

    for season_id in season_ids:
        try:
            matches = maclari_al(
                tournament_id=tournament_id, season_id=season_id, by_date=by_date
            )

            processed_list = []
            for m in matches:
                processed = mac_verisini_isle(m, insert_to_mongo=False)
                if processed is not None:
                    processed_list.append(processed)

            if processed_list:
                insert_table_df(pd.DataFrame(processed_list), table_name="match")

            match_ids = list(dict.fromkeys(_extract_match_ids(processed_list)))

            for payload in PAYLOAD_TABLE_MAP:
                _run_payload(payload, match_ids, season_id, summary["errors"])

            summary["seasons"][str(season_id)] = {
                "fetched_matches": len(matches) if matches else 0,
                "processed_matches": len(processed_list),
                "match_ids": match_ids,
            }

        except Exception as e:
            logger.exception(f"Pipeline error for season {season_id}: {e}")
            summary["errors"].append(str(e))

    return summary
