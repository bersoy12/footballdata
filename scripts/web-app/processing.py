
from typing import List, Dict
from scraper import get_round_matches, get_match_events, get_tournaments, get_match_statistics, get_match_graph
import logging

logger = logging.getLogger(__name__)

def process_tournament(tournament):
    return {"id": tournament.get("id"), "name": tournament.get("name")}

def process_match(match):
    return {"match_id": match.get("id")
                    , "tournament_id": match.get("tournament").get("id")
                    , "season_id": match.get("season").get("id")
                    , "round": match.get("roundInfo").get("round")
                    , "start_timestamp": match.get("startTimestamp")
                    , "home_team_id": match.get("homeTeam").get("id")
                    , "home_team_name": match.get("homeTeam").get("name")
                    , "away_team_id": match.get("awayTeam").get("id")
                    , "away_team_name": match.get("awayTeam").get("name")
                    # , "slug": match.get("slug")
                    , "status_code": match.get("status").get("code")
                    , "status_type": match.get("status").get("type")
                    , "winner_code": match.get("winnerCode")
                    , "home_score_period1": match.get("homeScore").get("period1")
                    , "home_score_period2": match.get("homeScore").get("period2")
                    , "home_score_normaltime": match.get("homeScore").get("normaltime")
                    , "away_score_period1": match.get("awayScore").get("period1")
                    , "away_score_period2": match.get("awayScore").get("period2")
                    , "away_score_normaltime": match.get("awayScore").get("normaltime")
                    , "time_injury_time1": match.get("time").get("injuryTime1")
                    , "time_injury_time2": match.get("time").get("injuryTime2")}


def process_match_data(match) -> tuple:
    """Tek bir maç için tüm verileri işler"""

    match_id = match.get('id')
    if match.get("status", {}).get("type") == "notstarted":
        logger.info(f"Maç {match_id} başlamadı, atlanıyor.")
        return None

    logger.info(f"Maç {match_id} için veriler işleniyor...")
    
    match_data = process_match(match)
    
    return match_data


def process_statistics(statistics, match_id):
    """İstatistiksel maç verilerini düzleştirir."""
    flattened_data = []
    periods = statistics.get("statistics")
    for period in periods:
        period_name = period.get("period")
        groups = period.get("groups")
        for group in groups:
            group_name = group.get("groupName")
            stat_items = group.get("statisticsItems")
            for item in stat_items:
                stats = {
                        "match_id": match_id,
                        "period": period_name,
                        "group_name": group_name,
                        "statistics_name": item.get("name"),
                        "home_value": item.get("home"),
                        "away_value": item.get("away"),
                        "key": item.get("key"),
                        "statistics_type": item.get("statisticsType"),
                        "value_type": item.get("valueType")
                    }
                flattened_data.append(stats)

    return flattened_data
    

def process_incidents(incidents, match_id):
    flattened_data = []
    incidents = incidents.get("incidents")
    for incident in incidents:
        data = {'match_id': match_id
                ,'incident_id': incident.get('id', None)
                ,'time': incident.get('time', None)
                ,'incident_class': incident.get('incidentClass', None)
                ,'reason': incident.get('reason', None)
                ,'incident_type': incident.get('incidentType', None)
                ,'text_': incident.get('text', None)
                ,'home_score': incident.get('homeScore', None)
                ,'away_score': incident.get('awayScore', None)
                ,'added_time': incident.get('addedTime', None)
                ,'length_': incident.get('length', None)
                ,'player_in_name': incident.get('playerIn', {}).get('name')
                ,'player_in_id': incident.get('playerIn', {}).get('id')
                ,'player_out_name': incident.get('playerOut', {}).get('name')
                ,'player_out_id': incident.get('playerOut', {}).get('id')
                ,'injury': incident.get('injury')
                ,'rescinded': incident.get('rescinded', False)
                ,'card_player_name': incident.get('player', {}).get('name')
                ,'card_player_id': incident.get('player', {}).get('id')
                ,'from_': incident.get('from', None)
                ,'scorer_name': incident.get('player', {}).get('name')
                ,'scorer_id': incident.get('player', {}).get('id')
                ,'assist1_name': incident.get('assist1', {}).get('name')
                ,'assist1_id': incident.get('assist1', {}).get('id')
                ,'confirmed': incident.get('confirmed', None)
                ,'var_player': incident.get('player', {}).get('name', None)
                ,'passing_network': incident.get('footballPassingNetworkAction', {})}
        flattened_data.append(data)

    return flattened_data


def process_graphs(graphs, match_id):
    flattened_data = []
    graph = graphs.get("graphPoints")
    for item in graph:
        data = {'match_id': match_id
                , 'minute': item.get("minute")
                , 'value': item.get("value")}
        flattened_data.append(data)

    return flattened_data


    