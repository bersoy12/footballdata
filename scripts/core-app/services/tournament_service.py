from data.scraper import get_country_info, get_unique_tournaments, get_tournaments
from processing import process_categories, process_unique_tournaments, process_tournaments
from data.db import insert_table_df
import pandas as pd


def ulke_bilgisi_getir():
    categories = get_country_info()
    return process_categories(categories)

def turnuvalari_getir(country_id: int, date: str = ""):
    tournaments = get_tournaments(country_id, date)
    return process_tournaments(tournaments, date)

def unique_tournaments_getir(country_id: int):
    tournaments = get_unique_tournaments(country_id)
    return process_unique_tournaments(tournaments)

