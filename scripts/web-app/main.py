from fastapi import FastAPI, Body, Query
from scraper import get_round_matches, get_match_events, get_tournaments, get_match_statistics, get_match_graph
from processing import process_statistics, process_incidents, process_match, process_tournament, process_match_data, process_graphs
from enum import Enum
import pandas as pd
from typing import List, Dict, Optional
from sql_alchemy import insert_table, does_exist, truncate_table, fetch_data
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

class PayloadType(str, Enum):
    statistics = "İstatistik"
    graphs = "Momentum Grafiği"


@app.post("/veri-cek")
def veri_cek_endpoint(
    tournament_id: Optional[int] = None,
    country_alpha: Optional[str] = None,
    season_id: Optional[int] = None, 
    start_week: Optional[int] = None, 
    end_week: Optional[int] = None, 
    update_tournaments: Optional[bool] = False
):
    """
    Belirli bir lig ve sezon için haftalık maç verilerini paralel olarak işler ve veritabanına kaydeder.
    """
    return veri_cek(tournament_id, country_alpha, season_id, start_week, end_week, update_tournaments)


@app.get("/maclari-al")
def maclari_al_endpoint(
    tournament_id: Optional[int] = None,
    season_id: Optional[int] = None, 
    week: Optional[int] = None,
    start_week: Optional[int] = None,
    end_week: Optional[int] = None,
):
    """
    Belirtilen hafta ya da haftalarda oynanan tüm maçları çeker.
    """
    if start_week:
        matches = []
        for week in range(start_week, end_week + 1):
            logger.info(f"Hafta {week} maçları alınıyor...")
            matches += maclari_al(tournament_id, season_id, week)

        return matches

    return maclari_al(tournament_id, season_id, week)


def maclari_al(tournament_id: Optional[int] = None,
               season_id: Optional[int] = None,
               week: Optional[int] = None):
    return get_round_matches(tournament_id, season_id, week)


@app.post("/mac-verisini-isle")
def mac_verisini_isle_endpoint(matches: List = Body(...)):
    maclar = []
    for match in matches:
        maclar.extend([mac_verisini_isle(match)])
    return maclar


def mac_verisini_isle(match):
    """Tek bir maç alır."""
    return process_match_data(match)
    

@app.post("/veritabanina-ekle")
def veritabanina_ekle_endpoint(
    table_name: str,
    data: List[Dict] = Body(...),
    on_conflict_columns: Optional[List[str]] = Query(default=[])
):
    lst_of_data = [item for item in data if item is not None]
    df = pd.DataFrame(lst_of_data)
    return varitabanina_ekle(df, table_name=table_name, on_conflict_columns=on_conflict_columns)

def varitabanina_ekle(df: pd.DataFrame, table_name: str, on_conflict_columns: Optional[List[str]] = [], on_conflict_entire_columns: Optional[bool] = False):
    return insert_table(df, table_name=table_name, on_conflict_columns=on_conflict_columns, on_conflict_entire_columns=on_conflict_entire_columns)


@app.post("/istatistikleri-al")
def istatistikleri_al_endpoint(
    match_ids: List[int] = Body(...),
    payload: PayloadType = Query(..., embed=True),
    insert_simultaneously: bool = True
):
    """
    Birden fazla maç için istatistikleri/grafikleri paralel olarak işler. Simultane bir şekilde veri tabanına yükler.
    """
    if payload == "İstatistik":
        with ThreadPoolExecutor(max_workers=1) as executor:
            processed_stats = list(executor.map(
                lambda match_id: mac_istatistiklerini_isle(match_id, insert_simultaneously),
                match_ids
            ))

        stats = list(chain.from_iterable(processed_stats))
        return stats

    if payload == "Momentum Grafiği":
        with ThreadPoolExecutor(max_workers=1) as executor:
            processed_graphs = list(executor.map(
                lambda match_id: mac_grafiklerini_isle(match_id, insert_simultaneously),
                match_ids
            ))

        graphs = list(chain.from_iterable(processed_graphs))
        return graphs
    
    return None



def mac_grafiklerini_isle(match_id: int, insert_simultaneously: bool = True):
    graphs = get_match_graph(match_id)
    processed_graphs = process_graphs(graphs, match_id)
    if processed_graphs == []:
        return []
    if insert_simultaneously:
        varitabanina_ekle(pd.DataFrame(processed_graphs), table_name="momentum", on_conflict_entire_columns = False)
    return processed_graphs



def mac_istatistiklerini_isle(match_id: int, insert_simultaneously: bool = True):
    stats = get_match_statistics(match_id)
    processed_stats = process_statistics(stats, match_id)
    if processed_stats == []:
        return []
    if insert_simultaneously:
        varitabanina_ekle(pd.DataFrame(processed_stats), table_name="statistic", on_conflict_entire_columns = False)
    return processed_stats




@app.get("/veritabanindan-cek")
def veritabanindan_cek_endpoint(
    table_name: str,
    column_name: str
    ):

    return veritabanindan_cek(table_name, column_name)

def veritabanindan_cek(
    table_name: str,
    column_name: str
        ):
    return fetch_data(column_name, table_name)

def veri_cek(tournament_id: int = None,
         country_alpha: str = None,
         season_id: int = None, 
         start_week: int = None, 
         end_week: int = None, 
         update_tournaments: bool = False,
         update_statistic: bool = False):
    """
    Belirli bir lig ve sezon için haftalık maç verilerini paralel olarak işler ve veritabanına kaydeder.
    """
    # Veritabanı bağlantısını bir kere oluştur
    # conn, cursor = connect_postgre("football")
    # if conn is None or cursor is None:
    #     logger.info("Veritabanı bağlantısı kurulamadı!")
    #     return

    # try:
    #     if tournament_id is not None:
    #         exist = does_exist(tournament_id, column_name="id", table_name="tournament")
    #         if not exist:
    #             tournaments = get_tournaments(country_alpha)[["id","name"]]
    #             insert_table(tournaments, table_name="tournament", on_conflict_columns=["id"])

    #             # all_tournaments = []
    #             # for tournament in tournaments:
    #             #     all_tournaments.append(process_tournament(tournament))

    #         # batch_insert(conn, cursor, "tournament", all_tournaments)
    # except Exception as e:
    #     logger.info(f"İşlem sırasında hata oluştu: {str(e)}")

    try:
        # Tüm haftaların maçlarını topla
        all_matches = []
        for week in range(start_week, end_week + 1):
            logger.info(f"Hafta {week} maçları alınıyor...")
            try:
                matches = get_round_matches(tournament_id, season_id, week)
            except:
                matches = None
            if matches == [] or matches == None:
                continue
            all_matches.extend(matches)

        with ThreadPoolExecutor(max_workers=1) as executor:
            results = list(executor.map(process_match_data, all_matches))
        
        logger.info("Maçlar işlendi.")
        logger.info("Maçlar veritabanına yükleniyor.")
        insert_table(pd.DataFrame(results), table_name="match", on_conflict_columns=["match_id"])
        
        # maç tablosunda bulunan match idleri al
        logger.info("Maç tablosundan match_id'leri alınıyor.")
        match_ids = fetch_data("match_id", "match")

    
        # match stats

        logger.info("İstatistikler çekiliyor.")

        # statistics tablosunda eğer o maç idsi yoksa maç istatistiklerini al
        
        statistics_match_ids = fetch_data("match_id", "statistic")
        match_ids_for_stats = list(set(match_ids) ^ set(statistics_match_ids))

        logger.info(f"Bu maçlar için işlem yapılıyor: {match_ids_for_stats}")

        with ThreadPoolExecutor(max_workers=1) as executor:
            statistics = list(executor.map(get_match_statistics, match_ids_for_stats))

        with ThreadPoolExecutor(max_workers=1) as executor:
            game_stats = list(executor.map(process_statistics, statistics, match_ids_for_stats))

        game_stats = list(chain.from_iterable(game_stats))
        try:
            insert_table(pd.DataFrame(game_stats), table_name="statistic")
        except Exception as e:
            logger.info(f"insert_table statistic sırasında hata oluştu: {str(e)}")


        logger.info("Olaylar çekiliyor.")

        # match incidents

        incident_match_ids  = fetch_data("match_id", "incident")

        match_ids_for_incident = list(set(match_ids) ^ set(incident_match_ids))

        logger.info(f"Bu maçlar için işlem yapılıyor: {match_ids_for_incident}")

        with ThreadPoolExecutor(max_workers=1) as executor:
            events = list(executor.map(get_match_events, match_ids_for_incident))

        with ThreadPoolExecutor(max_workers=1) as executor:
            game_events = list(executor.map(process_incidents, events, match_ids_for_incident))

        game_events = list(chain.from_iterable(game_events))
        try:
            insert_table(pd.DataFrame(game_events), table_name="incident")
        except Exception as e:
            logger.info(f"insert_table incident sırasında hata oluştu: {str(e)}")


        logger.info("Grafikler çekiliyor.")
        # match momentum

        graph_match_ids = fetch_data("match_id", "momentum")

        match_ids_for_momentum = list(set(match_ids) ^ set(graph_match_ids))

        logger.info(f"Bu maçlar için işlem yapılıyor: {match_ids_for_momentum}")

        with ThreadPoolExecutor(max_workers=1) as executor:
            graphs = list(executor.map(get_match_graph, match_ids_for_momentum))

        with ThreadPoolExecutor(max_workers=1) as executor:
            game_graphs = list(executor.map(process_graphs, graphs, match_ids_for_momentum))

        game_graphs = list(chain.from_iterable(game_graphs))
        try:
            insert_table(pd.DataFrame(game_graphs), table_name="momentum")
        except Exception as e:
            logger.info(f"insert_table match_momentum sırasında hata oluştu: {str(e)}")

        

    
        # return statistics, events, graphs, match_ids, game_stats, game_events, game_graphs



    except Exception as e:
        logger.info(f"İşlem sırasında hata oluştu: {str(e)}")
    finally:
        pass





