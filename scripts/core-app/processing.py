
from typing import List, Dict
from scraper import get_round_matches, get_match_events, get_top_tournaments, get_match_statistics, get_match_graph
import logging

logger = logging.getLogger(__name__)

def process_team_stats(team_stats, team_id, tournament_id, season_id):
    """Takım istatistiklerini düzleştirir."""
    if not team_stats:
        return []
    
    flattened_data = []
    row = team_stats.get("statistics", {})
    flattened_data = {
                "team_id" : team_id,
                "tournament_id" : tournament_id,
                "season_id" : season_id,
                "goals_scored" : row.get("goalsScored"),
                "goals_conceded" : row.get("goalsConceded"),
                "own_goals" : row.get("ownGoals"),
                "assists" : row.get("assists"),
                "shots" : row.get("shots"),
                "penalty_goals" : row.get("penaltyGoals"),
                "penalties_taken" : row.get("penaltiesTaken"),
                "free_kick_goals" : row.get("freeKickGoals"),
                "free_kick_shots" : row.get("freeKickShots"),
                "goals_from_inside_the_box" : row.get("goalsFromInsideTheBox"),
                "goals_from_outside_the_box" : row.get("goalsFromOutsideTheBox"),
                "shots_from_inside_the_box" : row.get("shotsFromInsideTheBox"),
                "shots_from_outside_the_box" : row.get("shotsFromOutsideTheBox"),
                "headed_goals" : row.get("headedGoals"),
                "left_foot_goals" : row.get("leftFootGoals"),
                "right_foot_goals" : row.get("rightFootGoals"),
                "big_chances" : row.get("bigChances"),
                "big_chances_created" : row.get("bigChancesCreated"),
                "big_chances_missed" : row.get("bigChancesMissed"),
                "shots_on_target" : row.get("shotsOnTarget"),
                "shots_off_target" : row.get("shotsOffTarget"),
                "blocked_scoring_attempt" : row.get("blockedScoringAttempt"),
                "successful_dribbles" : row.get("successfulDribbles"),
                "dribble_attempts" : row.get("dribbleAttempts"),
                "corners" : row.get("corners"),
                "hit_woodwork" : row.get("hitWoodwork"),
                "fast_breaks" : row.get("fastBreaks"),
                "fast_break_goals" : row.get("fastBreakGoals"),
                "fast_break_shots" : row.get("fastBreakShots"),
                "average_ball_possession" : row.get("averageBallPossession"),
                "total_passes" : row.get("totalPasses"),
                "accurate_passes" : row.get("accuratePasses"),
                "accurate_passes_percentage" : row.get("accuratePassesPercentage"),
                "total_own_half_passes" : row.get("totalOwnHa0lfPasses"),
                "accurate_own_half_passes" : row.get("accurateOwnHalfPasses"),
                "accurate_own_half_passes_percentage" : row.get("accurateOwnHalfPassesPercentage"),
                "total_opposition_half_passes" : row.get("totalOppositionHalfPasses"),
                "accurate_opposition_half_passes" : row.get("accurateOppositionHalfPasses"),
                "accurate_opposition_half_passes_percentage" : row.get("accurateOppositionHalfPassesPercentage"),
                "total_long_balls" : row.get("totalLongBalls"),
                "accurate_long_balls" : row.get("accurateLongBalls"),
                "accurate_long_balls_percentage" : row.get("accurateLongBallsPercentage"),
                "total_crosses" : row.get("totalCrosses"),
                "accurate_crosses" : row.get("accurateCrosses"),
                "accurate_crosses_percentage" : row.get("accurateCrossesPercentage"),
                "clean_sheets" : row.get("cleanSheets"),
                "tackles" : row.get("tackles"),
                "interceptions" : row.get("interceptions"),
                "saves" : row.get("saves"),
                "errors_leading_to_goal" : row.get("errorsLeadingToGoal"),
                "errors_leading_to_shot" : row.get("errorsLeadingToShot"),
                "penalties_committed" : row.get("penaltiesCommited"),
                "penalty_goals_conceded" : row.get("penaltyGoalsConceded"),
                "clearances" : row.get("clearances"),
                "clearances_off_line" : row.get("clearancesOffLine"),
                "last_man_tackles" : row.get("lastManTackles"),
                "total_duels" : row.get("totalDuels"),
                "duels_won" : row.get("duelsWon"),
                "duels_won_percentage" : row.get("duelsWonPercentage"),
                "total_ground_duels" : row.get("totalGroundDuels"),
                "ground_duels_won" : row.get("groundDuelsWon"),
                "ground_duels_won_percentage" : row.get("groundDuelsWonPercentage"),
                "total_aerial_duels" : row.get("totalAerialDuels"),
                "aerial_duels_won" : row.get("aerialDuelsWon"),
                "aerial_duels_won_percentage" : row.get("aerialDuelsWonPercentage"),
                "possession_lost" : row.get("possessionLost"),
                "offsides" : row.get("offsides"),
                "fouls" : row.get("fouls"),
                "yellow_cards" : row.get("yellowCards"),
                "yellow_red_cards" : row.get("yellowRedCards"),
                "red_cards" : row.get("redCards"),
                "avg_rating" : row.get("avgRating"),
                "accurate_final_third_passes_against" : row.get("accurateFinalThirdPassesAgainst"),
                "accurate_opposition_half_passes_against" : row.get("accurateOppositionHalfPassesAgainst"),
                "accurate_own_half_passes_against" : row.get("accurateOwnHalfPassesAgainst"),
                "accurate_passes_against" : row.get("accuratePassesAgainst"),
                "big_chances_against" : row.get("bigChancesAgainst"),
                "big_chances_created_against" : row.get("bigChancesCreatedAgainst"),
                "big_chances_missed_against" : row.get("bigChancesMissedAgainst"),
                "clearances_against" : row.get("clearancesAgainst"),
                "corners_against" : row.get("cornersAgainst"),
                "crosses_successful_against" : row.get("crossesSuccessfulAgainst"),
                "crosses_total_against" : row.get("crossesTotalAgainst"),
                "dribble_attempts_total_against" : row.get("dribbleAttemptsTotalAgainst"),
                "dribble_attempts_won_against" : row.get("dribbleAttemptsWonAgainst"),
                "errors_leading_to_goal_against" : row.get("errorsLeadingToGoalAgainst"),
                "errors_leading_to_shot_against" : row.get("errorsLeadingToShotAgainst"),
                "hit_woodwork_against" : row.get("hitWoodworkAgainst"),
                "interceptions_against" : row.get("interceptionsAgainst"),
                "key_passes_against" : row.get("keyPassesAgainst"),
                "long_balls_successful_against" : row.get("longBallsSuccessfulAgainst"),
                "long_balls_total_against" : row.get("longBallsTotalAgainst"),
                "offsides_against" : row.get("offsidesAgainst"),
                "red_cards_against" : row.get("redCardsAgainst"),
                "shots_against" : row.get("shotsAgainst"),
                "shots_blocked_against" : row.get("shotsBlockedAgainst"),
                "shots_from_inside_the_box_against" : row.get("shotsFromInsideTheBoxAgainst"),
                "shots_from_outside_the_box_against" : row.get("shotsFromOutsideTheBoxAgainst"),
                "shots_off_target_against" : row.get("shotsOffTargetAgainst"),
                "shots_on_target_against" : row.get("shotsOnTargetAgainst"),
                "blocked_scoring_attempt_against" : row.get("blockedScoringAttemptAgainst"),
                "tackles_against" : row.get("tacklesAgainst"),
                "total_final_third_passes_against" : row.get("totalFinalThirdPassesAgainst"),
                "opposition_half_passes_total_against" : row.get("oppositionHalfPassesTotalAgainst"),
                "own_half_passes_total_against" : row.get("ownHalfPassesTotalAgainst"),
                "total_passes_against" : row.get("totalPassesAgainst"),
                "yellow_cards_against" : row.get("yellowCardsAgainst"),
                "throw_ins" : row.get("throwIns"),
                "goal_kicks" : row.get("goalKicks"),
                "ball_recovery" : row.get("ballRecovery"),
                "free_kicks" : row.get("freeKicks"),
                "matches" : row.get("matches"),
                "id": row.get("id"),
                "awarded_matches" : row.get("awardedMatches")
            }
        
    return [flattened_data]


def process_teams_from_standing(data):
    teams = []
    if data[0].get("type") == "total":
        country_id = data[0].get("tournament").get("category").get("id")
        tournament_id = data[0].get("tournament").get("id")
        unique_tournament_id = data[0].get("tournament").get("uniqueTournament").get("id")
        for row in data[0].get("rows"):
            teams += [{"team_id": row.get("team").get("id")
                , "team_name": row.get("team").get("name")
                , "name_code": row.get("team").get("nameCode")
                , "sport_name": row.get("team").get("sport").get("name")
                , "disabled": row.get("team").get("disabled")
                , "national": row.get("team").get("national")
                , "sport_id": row.get("team").get("sport").get("id")
                # , "country": row.get("team").get("country").get("name")
                , "team_colors_primary": row.get("team").get("teamColors").get("primary")
                , "team_colors_secondary": row.get("team").get("teamColors").get("secondary")
                , "country_id": country_id
                , "tournament_id": tournament_id
                , "unique_tournament_id": unique_tournament_id
            }]
    return teams


def process_tournaments(data, date):
    tournaments = []
    if data:
        for row in data:
            tournaments += [{"country_id": row.get("tournament").get("category").get("id")
                , "tournament_name": row.get("tournament").get("name")
                , "tournament_id": row.get("tournament").get("id")
                , "sport": row.get("tournament").get("category").get("sport").get("name")
                , "season_id": row.get("season", {}).get("id", "")
                , "season_year": row.get("season", {}).get("year", "")
                , "season_name": row.get("season", {}).get("name", "")
                , "round_info": row.get("roundInfo", {}).get("round", "")
                , "gender": row.get("eventFilters", {}).get("gender", [""])[0]
                , "date": date
            }]
    else:
        return []
    return list({v['season_id']:v for v in tournaments}.values())


def process_unique_tournaments(data):
    tournaments = []
    for row in data:
        tournaments += [{"country_id": row.get("category").get("id")
            , "unique_tournament_id": row.get("id")
            , "tournament_name": row.get("name")
            , "sport_id": row.get('category').get("sport").get("id")
            , "sport_name": row.get('category').get("sport").get("name")
            }]
    return tournaments


def process_match(match):
    return {"match_id": match.get("id")
                    , "tournament_id": match.get("tournament").get("id")
                    , "unique_tournament_id": match.get("tournament").get("uniqueTournament").get("id")
                    # , "tournament_name": match.get("tournament").get("name")
                    # , "country_name": match.get("tournament").get("category").get("name")
                    , "country_id": match.get("tournament").get("category").get("id")
                    # , "alpha2": match.get("tournament").get("category").get("country").get("alpha2")
                    # , "sport": match.get("tournament").get("category").get("sport").get("name")
                    # , "season_year": match.get("season").get("year")
                    , "season_id": match.get("season").get("id")
                    , "round": match.get("roundInfo", {"round": None}).get("round")
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
        logger.info(f"Match {match_id} has not started. Skipping.")
        return None

    logger.info(f"Processing data for match {match_id}...")
    
    match_data = process_match(match)
    return match_data


def process_statistics(statistics, match_id):
    """İstatistiksel maç verilerini düzleştirir."""
    if not statistics:
        return []
    # if statistics.get("error").get("code") == 404:
    #     logger.info(f"{match_id}" + " " + statistics.get("error").get("message"))
    #     return []
    
    flattened_data = []
    periods = statistics.get("statistics", {})
    if periods == {}:
        logger.info(f'{match_id} {statistics.get("error").get("message")} Error code: {str(statistics.get("error").get("code"))}')
        return []
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


def process_categories(data):
    countries = []
    for row in data:
        countries += [{
            "country_id": row.get("id"),
            "country_name": row.get("name"),
            "country_alpha2": row.get("alpha2", None)
            }]
    return countries
        
        

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
    graph = graphs.get("graphPoints", {})

    if graph == {}:
        logger.info(f'{match_id} {graphs.get("error").get("message")} Error code: {str(graphs.get("error").get("code"))}')
        return []
    
    for item in graph:
        data = {'match_id': match_id
                , 'minute': item.get("minute")
                , 'value': item.get("value")}
        flattened_data.append(data)

    return flattened_data


def process_seasons(data, unique_tournament_id):
    seasons = []
    
    for season in data:
        seasons += [{
            "season_id": season.get("id")
            , "name": season.get("name")
            , "year": season.get("year")
            , "unique_tournament_id": unique_tournament_id
        }]

    return seasons