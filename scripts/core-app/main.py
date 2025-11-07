from fastapi import FastAPI, Body, Query
from scraper import get_round_matches, get_match_events, get_team_statistics, get_match_statistics, get_match_graph, get_country_info, get_top_tournaments, get_rounds_unique_tournament, get_tournaments_by_country
from processing import process_statistics, process_incidents, process_match, process_match_data, process_graphs, process_categories, process_tournaments, process_team_stats
from enum import Enum
import pandas as pd
from typing import List, Dict, Optional, Any
from sql_alchemy import insert_table, fetch_data
from mongodb_client import mongodb_client
from concurrent.futures import ThreadPoolExecutor
from cloudflarescraper import CloudflareScraper
from itertools import chain
import logging
import json
import time
from typing import Union

def serialize_mongo_document(doc):
    doc["_id"] = str(doc["_id"])
    return doc

logger = logging.getLogger(__name__)

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})


class PayloadType(str, Enum):
    statistics = "İstatistik"
    graphs = "Momentum Grafiği"
    events = "Olaylar"


@app.post("/scape-website")
async def scrape_website_endpoint(url: str = Body(..., embed=True)):
    scraper_instance = CloudflareScraper()
    result = scraper_instance.scrape_website(url)
    return result


# --- Orchestration pipeline ----
def _extract_match_ids_from_response(resp: Union[dict, list]) -> list:
    """Recursively extract all match_id values from nested JSON using JSONPath-like traversal.
    Implements a simple search for keys named 'match_id' anywhere in the structure.
    """
    ids = []
    if isinstance(resp, dict):
        for k, v in resp.items():
            if k == 'match_id' and (isinstance(v, int) or (isinstance(v, str) and v.isdigit())):
                ids.append(int(v))
            else:
                ids.extend(_extract_match_ids_from_response(v))
    elif isinstance(resp, list):
        for item in resp:
            ids.extend(_extract_match_ids_from_response(item))
    return ids


@app.post('/pipeline/run')
def pipeline_run_endpoint(
    tournament_id: Optional[int] = Body(None),
    season_ids: Optional[List[int]] = Body(None),
    by_date: bool = Body(True)
):
    """Orchestrates the full flow you described for one tournament across one or many seasons.

    Behavior:
    1. Calls internal maclari_al to fetch rounds (by_date if specified).
    2. Sends response(s) to mac_verisini_isle (internal function) to process data.
    3. Inserts processed matches into 'match' table via varitabanina_ekle wrapper.
    4. Extracts match_ids from processed data.
    5. Calls veri-topla three times for payloads: İstatistik, Momentum Grafiği, Olaylar with insert_simultaneously=True.

    Returns a summary dict with counts and any errors encountered.
    """
    summary = {
        'tournament_id': tournament_id,
        'seasons': {},
        'errors': []
    }

    if not tournament_id:
        return {"error": "tournament_id is required"}

    if not season_ids:
        season_ids = [None]

    for season_id in season_ids:
        try:
            # 1. fetch matches
            matches = maclari_al(tournament_id=tournament_id, season_id=season_id, by_date=by_date)

            # 2. process each match through mac_verisini_isle (reuse existing function)
            processed_list = []
            for m in matches:
                processed = mac_verisini_isle(m, insert_to_mongo=False)
                if processed is not None:
                    processed_list.append(processed)

            # 3. insert into 'match' table
            if processed_list:
                df = pd.DataFrame(processed_list)
                varitabanina_ekle(df, table_name='match')

            # 4. extract match_ids
            match_ids = _extract_match_ids_from_response(processed_list)
            # dedupe
            match_ids = list(dict.fromkeys(match_ids))

            # 5. call veri-topla three times, but skip match_ids that already exist in the target tables
            payloads = ['İstatistik', 'Momentum Grafiği', 'Olaylar']
            table_map = {'İstatistik': 'statistic', 'Momentum Grafiği': 'momentum', 'Olaylar': 'incident'}
            for payload in payloads:
                try:
                    if not match_ids:
                        logger.info(f"No match_ids to process for payload {payload} (season {season_id}).")
                        continue

                    target_table = table_map.get(payload)
                    # fetch existing match_ids from DB for this table
                    try:
                        existing = fetch_data('match_id', target_table)
                    except Exception:
                        existing = None

                    existing_ids = set()
                    if existing:
                        # fetch_data may return list of ints or list of dicts
                        for item in existing:
                            if isinstance(item, dict):
                                # try common shapes
                                if 'match_id' in item:
                                    val = item.get('match_id')
                                else:
                                    # fallback: take first value
                                    vals = list(item.values())
                                    val = vals[0] if vals else None
                            else:
                                val = item
                            try:
                                existing_ids.add(int(val))
                            except Exception:
                                continue

                    # remove ids that are already present
                    to_process = [mid for mid in match_ids if mid not in existing_ids]
                    if not to_process:
                        logger.info(f"All match_ids already present for table {target_table}; skipping payload {payload} for season {season_id}.")
                        continue

                    # call the processing endpoint internally for remaining match ids
                    istatistikleri_al_endpoint(to_process, payload=PayloadType(payload), insert_simultaneously=True, insert_to_mongo=False)

                except Exception as e:
                    logger.error(f"Error while running payload {payload} for season {season_id}: {e}")
                    summary['errors'].append(str(e))

            summary['seasons'][str(season_id)] = {
                'fetched_matches': len(matches) if matches else 0,
                'processed_matches': len(processed_list),
                'match_ids': match_ids
            }

        except Exception as e:
            logger.exception(f"Pipeline error for season {season_id}: {e}")
            summary['errors'].append(str(e))

    return summary


@app.get('/ulke-bilgisi-getir')
def ulke_bilgisi_getir_endpoint():
    return ulke_bilgisi_getir()


def ulke_bilgisi_getir():
    categories = get_country_info()
    processed_categories = process_categories(categories)
    return processed_categories


@app.get('/ligleri-getir')
def ligleri_getir_endpoint(
    country_id: int
    ):
    return ligleri_getir(country_id)
    

def ligleri_getir(country_id: int):
    tournaments = get_tournaments_by_country(country_id)
    processed_tournaments = process_tournaments(tournaments)
    return processed_tournaments
    

@app.get('/takim-istatistiklerini-getir')
def takim_istatistiklerini_getir_endpoint(
    team_id: int,
    tournament_id: int,
    season_id: int,
    insert_to_db: bool = False
    ):
    team_stats = get_team_statistics(team_id, tournament_id, season_id)
    processed_team_stats = process_team_stats(team_stats, team_id, tournament_id, season_id)
    if insert_to_db:
        df = pd.DataFrame(processed_team_stats)
        varitabanina_ekle(df, table_name='team_statistics_overall')
    return processed_team_stats



@app.get("/maclari-al")
def maclari_al_endpoint(
    tournament_id: int = None,
    season_id: int = None, 
    week: Optional[int] = None,
    start_week: Optional[int] = None,
    end_week: Optional[int] = None,
    by_date: Optional[bool] = None,
    since_timestamp: Optional[int] = Query(default=None, description="Current timestamp {}".format(int(time.time())))
):
    """
    Belirtilen hafta ya da haftalarda oynanan tüm maçları çeker.
    """
    if by_date:
        logger.info(f"Günlük olarak maçlar alınıyor...")
        return maclari_al(tournament_id, season_id, by_date=by_date, since_timestamp=since_timestamp)
    elif start_week:
        matches = []
        for week in range(start_week, end_week + 1):
            try:
                logger.info(f"Hafta {week} maçları alınıyor...")
                matches += maclari_al(tournament_id, season_id, week)
            except:
                continue

        return matches
    
    return maclari_al(tournament_id, season_id, week)


def maclari_al(tournament_id: Optional[int] = None,
               season_id: Optional[int] = None,
               week: Optional[int] = None,
               by_date: Optional[bool] = None,
               since_timestamp: Optional[int] = None):
    """
    Belirli bir lig, sezon ve haftadaki maçları getirir.
    """
    if by_date:
        if since_timestamp:
            data = get_rounds_unique_tournament(tournament_id, season_id)
            filtered = [
                m for m in data["events"]
                if m.get("startTimestamp", 0) > since_timestamp
                ]
            return filtered
        return get_rounds_unique_tournament(tournament_id, season_id)
    return get_round_matches(tournament_id, season_id, week)


@app.post("/mac-verisini-isle")
def mac_verisini_isle_endpoint(matches: List = Body(...)
                               , insert_to_mongo: bool = Query(default=False)
                               , collection_name: str = None):
    maclar = []
    for match in matches:
        maclar.extend([mac_verisini_isle(match, insert_to_mongo=insert_to_mongo, collection_name=collection_name)])
    return maclar


def mac_verisini_isle(match, insert_to_mongo: bool = False, collection_name: str = None):
    """
    Tek bir maçın tüm verilerini işler ve uygun formata dönüştürür.
    """
    processed = process_match_data(match)
    if insert_to_mongo and processed and collection_name:
        data_list = processed if isinstance(processed, list) else [processed]
        result = mongodb_client.insert_bulk_raw_data(collection_name, data_list)
        logger.info(f"MongoDB insertion result: {result}")
    elif insert_to_mongo and not collection_name:
        logger.warning("insert_to_mongo is True but collection_name is None. Skipping MongoDB insertion.")
    if insert_to_mongo:
        return serialize_mongo_document(processed)
    else:
        return processed
    

@app.post("/veritabanina-ekle")
def veritabanina_ekle_endpoint(
    table_name: str,
    data: List[Dict] = Body(...),
    on_conflict_columns: Optional[List[str]] = Query(default=[])
):
    lst_of_data = [item for item in data if item is not None]
    df = pd.DataFrame(lst_of_data)
    logger.info(f"{len(df.index)} number of match is going to be processed.")
    return varitabanina_ekle(df, table_name=table_name, on_conflict_columns=on_conflict_columns)

def varitabanina_ekle(df: pd.DataFrame, table_name: str, on_conflict_columns: Optional[List[str]] = [], on_conflict_entire_columns: Optional[bool] = False):
    """
    Verilen verileri (DataFrame olarak) belirtilen tabloya ekler. Çakışma durumunda hangi sütunlara göre işlem yapılacağını belirtebilirsiniz.
    """
    return insert_table(df, table_name=table_name, on_conflict_columns=on_conflict_columns, on_conflict_entire_columns=on_conflict_entire_columns)


@app.post("/veri-topla")
def istatistikleri_al_endpoint(
    match_ids: List[int] = Body(...),
    payload: PayloadType = Query(..., embed=True),
    insert_simultaneously: bool = False,
    insert_to_mongo: bool = False
):
    """
    Birden fazla maç için istatistikleri/grafikleri paralel olarak işler. Simultane bir şekilde veri tabanına yükler.
    """
    if payload == "İstatistik":
        with ThreadPoolExecutor(max_workers=1) as executor:
            processed_stats = list(executor.map(
                lambda match_id: mac_istatistiklerini_isle(match_id, insert_simultaneously, insert_to_mongo),
                match_ids
            ))

        stats = list(chain.from_iterable(processed_stats))
        return None

    if payload == "Momentum Grafiği":
        with ThreadPoolExecutor(max_workers=1) as executor:
            processed_graphs = list(executor.map(
                lambda match_id: mac_grafiklerini_isle(match_id, insert_simultaneously, insert_to_mongo),
                match_ids
            ))

        graphs = list(chain.from_iterable(processed_graphs))
        return None

    if payload == "Olaylar":
        with ThreadPoolExecutor(max_workers=1) as executor:
            processed_events = list(executor.map(
                lambda match_id: mac_olaylarini_isle(match_id, insert_simultaneously, insert_to_mongo),
                match_ids
            ))

        events = list(chain.from_iterable(processed_events))
        return None
    
    return None


def mac_olaylarini_isle(match_id: int, insert_simultaneously: bool = False, insert_to_mongo: bool = False):
    events = get_match_events(match_id)
    processed_events = process_incidents(events, match_id)
    if processed_events == []:
        return []
    if insert_simultaneously:
        varitabanina_ekle(pd.DataFrame(processed_events), table_name="incident", on_conflict_entire_columns = False)
    if insert_to_mongo:
        insert_raw_data(collection_name="incident", data_list=processed_events)
    return processed_events



def mac_grafiklerini_isle(match_id: int, insert_simultaneously: bool = False, insert_to_mongo: bool = False):
    graphs = get_match_graph(match_id)
    processed_graphs = process_graphs(graphs, match_id)
    if processed_graphs == []:
        return []
    if insert_simultaneously:
        varitabanina_ekle(pd.DataFrame(processed_graphs), table_name="momentum", on_conflict_entire_columns = False)
    if insert_to_mongo:
        insert_raw_data(collection_name="momentum", data_list=processed_graphs)
    return processed_graphs



def mac_istatistiklerini_isle(match_id: int, insert_simultaneously: bool = False, insert_to_mongo: bool = False):
    stats = get_match_statistics(match_id)
    processed_stats = process_statistics(stats, match_id)
    if processed_stats == []:
        return []
    if insert_simultaneously:
        varitabanina_ekle(pd.DataFrame(processed_stats), table_name="statistic", on_conflict_entire_columns = False)
    if insert_to_mongo:
        insert_raw_data(collection_name="statistic", data_list=processed_stats)
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



# @app.post("/mongodb/raw-data")
# def mongodb_raw_data_endpoint(
#     collection_name: str,
#     data: Dict[str, Any] = Body(...)
# ):
#     """
#     Ham JSON verisini MongoDB'ye ekler
#     """
#     success = mongodb_client.insert_raw_data(collection_name, data)
#     return {"success": success, "collection": collection_name}


@app.post("/mongodb/insert-raw-data")
def mongodb_insert_raw_data_endpoint(
    collection_name: str,
    data_list: List[Dict[str, Any]] = Body(...)
):
    """
    Birden fazla ham JSON verisini MongoDB'ye toplu olarak ekler
    """
    return insert_raw_data(collection_name, data_list)


def insert_raw_data(collection_name: str, data_list: List[Dict[str, Any]]):
    result = mongodb_client.insert_bulk_raw_data(collection_name, data_list)
    logger.info(f"MongoDB insertion result: {result}")
    return {
        "success": result["successful"] > 0,
        "collection": collection_name,
        "successful": result["successful"],
        "failed": result["failed"]
    }


@app.get("/mongodb/raw-data")
def mongodb_get_raw_data_endpoint(
    collection_name: str
    , query: Optional[str] = Query(default=None, description="MongoDB query filter as JSON string (e.g., '{\"match_id\": 12345}')")
    , projection: Optional[str] = Query(default=None)
    , limit: int = Query(description="Maximum number of documents to return")
):
    """
    MongoDB'den ham veri çeker
    """
    query_dict = None
    projection_dict = None

    if query:
        try:
            query_dict = json.loads(query)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON query string: {e}")
            return {
                "error": "Invalid JSON query string",
                "collection": collection_name,
                "count": 0,
                "data": []
            }

    query_dict = None
    
    if projection:
        try:
            projection_dict = json.loads(projection)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON projection string: {e}")
            return {
                "error": "Invalid JSON projection string",
                "collection": collection_name,
                "count": 0,
                "data": []
            }
    
    data = mongodb_client.get_raw_data(collection_name, query_dict, projection_dict, limit)

    return {
        "collection": collection_name,
        "count": len(data),
        "data": data
    }


# @app.put("/mongodb/raw-data")
# def mongodb_update_raw_data_endpoint(
#     collection_name: str,
#     filter_query: Dict[str, Any] = Body(...),
#     update_data: Dict[str, Any] = Body(...)
# ):
#     """
#     MongoDB'deki ham veriyi günceller
#     """
#     success = mongodb_client.update_raw_data(collection_name, filter_query, update_data)
#     return {"success": success, "collection": collection_name}


# @app.delete("/mongodb/raw-data")
# def mongodb_delete_raw_data_endpoint(
#     collection_name: str,
#     filter_query: Dict[str, Any] = Body(...)
# ):
#     """
#     MongoDB'den ham veri siler
#     """
#     success = mongodb_client.delete_raw_data(collection_name, filter_query)
#     return {"success": success, "collection": collection_name}


@app.get("/mongodb/collections")
def mongodb_get_collections_endpoint():
    """
    Veritabanındaki tüm koleksiyonları listeler
    """
    collections = mongodb_client.get_collections()
    return {"collections": collections}


# @app.get("/mongodb/collection-stats/{collection_name}")
# def mongodb_get_collection_stats_endpoint(collection_name: str):
#     """
#     Koleksiyon istatistiklerini getirir
#     """
#     stats = mongodb_client.get_collection_stats(collection_name)
#     return stats





