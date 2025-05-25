from scraper import get_round_matches, get_match_events, get_tournaments, get_match_statistics, get_match_graph
from processing import process_statistics, process_incidents, process_match, process_tournament, process_match_data, process_graphs
import os
import pandas as pd
import concurrent.futures
from typing import List, Dict
from sql_alchemy import insert_table, does_exist, truncate_table, fetch_data
from concurrent.futures import ThreadPoolExecutor
from itertools import chain


def test(tournament_id: int = None,
         country_alpha: str = None,
         season_id: int = None, 
         start_week: int = None, 
         end_week: int = None, 
         update_tournaments: bool = False):
    """
    Belirli bir lig ve sezon için haftalık maç verilerini paralel olarak işler ve veritabanına kaydeder.
    """
    # Veritabanı bağlantısını bir kere oluştur
    # conn, cursor = connect_postgre("football")
    # if conn is None or cursor is None:
    #     print("Veritabanı bağlantısı kurulamadı!")
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
    #     print(f"İşlem sırasında hata oluştu: {str(e)}")

    try:
        # Tüm haftaların maçlarını topla
        all_matches = []
        for week in range(start_week, end_week + 1):
            print(f"Hafta {week} maçları alınıyor...")
            matches = get_round_matches(tournament_id, season_id, week)
            all_matches.extend(matches)

        with ThreadPoolExecutor(max_workers=1) as executor:
            results = list(executor.map(process_match_data, all_matches))
        
        print("Maçlar işlendi.")
        print("Maçlar veritabanına yükleniyor.")
        insert_table(pd.DataFrame(results), table_name="match", on_conflict_columns=["match_id"])
        
        # maç tablosunda bulunan match idleri al
        print("Maç tablosundan match_id'leri alınıyor.")
        match_ids = fetch_data("match_id", "match")

    

        # match stats

        print("İstatistikler çekiliyor.")

        # statistics tablosunda eğer o maç idsi yoksa maç istatistiklerini al
        statistics_match_ids = fetch_data("match_id", "statistic")

        match_ids_for_stats = list(set(match_ids) ^ set(statistics_match_ids))

        print("Bu maçlar için işlem yapılıyor: {match_ids_for_stats}")
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            statistics = list(executor.map(get_match_statistics, match_ids_for_stats))

        with ThreadPoolExecutor(max_workers=1) as executor:
            game_stats = list(executor.map(process_statistics, statistics, match_ids_for_stats))
        
        game_stats = list(chain.from_iterable(game_stats))
        try:
            insert_table(pd.DataFrame(game_stats), table_name="statistic")
        except Exception as e:
            print(f"insert_table statistic sırasında hata oluştu: {str(e)}")
        

        print("Olaylar çekiliyor.")

        # match incidents

        incident_match_ids  = fetch_data("match_id", "incident")

        match_ids_for_incident = list(set(match_ids) ^ set(incident_match_ids))

        print("Bu maçlar için işlem yapılıyor: {match_ids_for_incident}")

        with ThreadPoolExecutor(max_workers=1) as executor:
            events = list(executor.map(get_match_events, match_ids_for_incident))

        with ThreadPoolExecutor(max_workers=1) as executor:
            game_events = list(executor.map(process_incidents, events, match_ids_for_incident))

        game_events = list(chain.from_iterable(game_events))
        try:
            insert_table(pd.DataFrame(game_events), table_name="incident")
        except Exception as e:
            print(f"insert_table incident sırasında hata oluştu: {str(e)}")


        print("Grafikler çekiliyor.")
        # match momentum

        graph_match_ids = fetch_data("match_id", "momentum")

        match_ids_for_momentum = list(set(match_ids) ^ set(graph_match_ids))

        print("Bu maçlar için işlem yapılıyor: {match_ids_for_momentum}")

        with ThreadPoolExecutor(max_workers=1) as executor:
            graphs = list(executor.map(get_match_graph, match_ids_for_momentum))

        with ThreadPoolExecutor(max_workers=1) as executor:
            game_graphs = list(executor.map(process_graphs, graphs, match_ids_for_momentum))

        game_graphs = list(chain.from_iterable(game_graphs))
        try:
            insert_table(pd.DataFrame(game_graphs), table_name="momentum")
        except Exception as e:
            print(f"insert_table match_momentum sırasında hata oluştu: {str(e)}")

        

    
        return statistics, events, graphs, match_ids, game_stats, game_events, game_graphs



    except Exception as e:
        print(f"İşlem sırasında hata oluştu: {str(e)}")
    finally:
        pass



statistics, events, graphs, match_ids, game_stats, game_events, game_graphs = \
        test(tournament_id=52, country_alpha='TR', season_id=63814, start_week=1, end_week=38)


