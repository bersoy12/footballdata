import logging
import pandas as pd

from data.scraper import get_seasons
from processing import process_seasons
from data.db import insert_table_df

logger = logging.getLogger(__name__)


def sezonlari_isle(
    unique_tournament_id: int,
    insert_simultaneously: bool = False,
):
    seasons = get_seasons(unique_tournament_id)
    processed_seasons = process_seasons(seasons, unique_tournament_id)
    if not processed_seasons:
        return []
    if insert_simultaneously:
        insert_table_df(pd.DataFrame(processed_seasons), table_name="season")
    return processed_seasons
