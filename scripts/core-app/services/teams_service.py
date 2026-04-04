from data.scraper import get_teams
from processing import process_teams_from_standing


def takimlari_getir(unique_tournament_id: int, season_id: int):
    teams = get_teams(unique_tournament_id, season_id)
    return process_teams_from_standing(teams)