import logging
import pandas as pd
from typing import List

from data.scraper import get_match_events, get_match_statistics, get_match_graph, get_team_statistics
from processing import process_incidents, process_statistics, process_graphs, process_team_stats
from data.db import insert_table_df
from data.mongo import insert_bulk

logger = logging.getLogger(__name__)


def mac_olaylarini_isle(
    match_id: int,
    insert_simultaneously: bool = False,
    insert_to_mongo: bool = False,
) -> List[dict]:
    events = get_match_events(match_id)
    processed_events = process_incidents(events, match_id)
    if not processed_events:
        return []
    if insert_simultaneously:
        insert_table_df(pd.DataFrame(processed_events), table_name="incident")
    if insert_to_mongo:
        insert_bulk("incident", processed_events)
    return processed_events


def mac_istatistiklerini_isle(
    match_id: int,
    insert_simultaneously: bool = False,
    insert_to_mongo: bool = False,
) -> List[dict]:
    stats = get_match_statistics(match_id)
    processed_stats = process_statistics(stats, match_id)
    if not processed_stats:
        return []
    if insert_simultaneously:
        insert_table_df(pd.DataFrame(processed_stats), table_name="statistic")
    if insert_to_mongo:
        insert_bulk("statistic", processed_stats)
    return processed_stats


def mac_grafiklerini_isle(
    match_id: int,
    insert_simultaneously: bool = False,
    insert_to_mongo: bool = False,
) -> List[dict]:
    graphs = get_match_graph(match_id)
    processed_graphs = process_graphs(graphs, match_id)
    if not processed_graphs:
        return []
    if insert_simultaneously:
        insert_table_df(pd.DataFrame(processed_graphs), table_name="momentum")
    if insert_to_mongo:
        insert_bulk("momentum", processed_graphs)
    return processed_graphs


def takim_istatistiklerini_getir(
    team_id: int,
    unique_tournament_id: int,
    season_id: int,
    insert_to_db: bool = False,
):
    team_stats = get_team_statistics(team_id, unique_tournament_id, season_id)
    processed = process_team_stats(team_stats, team_id, unique_tournament_id, season_id)
    if insert_to_db:
        insert_table_df(pd.DataFrame(processed), table_name="team_statistics_overall")
    return processed