from cloudflarescraper import CloudflareScraper
import pandas as pd
import os
import json
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

UNIQUE_TOURNAMENTS_URL=os.getenv('UNIQUE_TOURNAMENTS_URL')
CATEGORIES_URL = os.getenv('CATEGORIES_URL')
TOP_TOURNAMENTS_URL = os.getenv('TOP_TOURNAMENTS_URL')
STANDINGS_URL = os.getenv('STANDINGS_URL')
ROUNDS_URL = os.getenv('ROUNDS_URL')
INCIDENTS_URL = os.getenv('INCIDENTS_URL')
STATISTICS_URL = os.getenv('STATISTICS_URL')
MOMENTUM_URL = os.getenv('MOMENTUM_URL')
UNIQUE_ROUND_URL = os.getenv('UNIQUE_ROUND_URL')
FEATURED_EVENTS_URL = os.getenv('FEATURED_EVENTS_URL')
SEASONS_URL = os.getenv('SEASONS_URL')
TEAM_STATS_URL = os.getenv('TEAM_STATS_URL')
SCHEDULED_EVENTS_URL = os.getenv('SCHEDULED_EVENTS_URL')
TEAMS_URL = os.getenv('TEAMS_URL')

scraper = CloudflareScraper()

def get_teams(unique_tournament_id: int, season_id: int) -> list:
    logger.info(f"Fetching teams for tournament {unique_tournament_id} season {season_id}.")
    try:
        response = scraper.scrape_website(TEAMS_URL.format(unique_tournament_id, season_id))
        if isinstance(response, dict) and 'error' in response:
            error = response['error']
            logger.error(f"API error {error.get('code')}: {error.get('message')}")
            return []
        data = response.get('standings')
        return data
    except Exception as e:
        logger.error(f"Error fetching teams: {e}")
        return []


def get_tournaments(country_id: int, date: str) -> list:
    logger.info(f"Fetching tournaments.")
    try:
        response = scraper.scrape_website(SCHEDULED_EVENTS_URL.format(country_id, date))
        if isinstance(response, dict) and 'error' in response:
            error = response['error']
            logger.error(f"API error {error.get('code')}: {error.get('message')}")
            return []
        data = response.get('events')
        return data
    except Exception as e:
        logger.error(f"Error fetching tournaments: {e}")
        return []


def get_country_info() -> list:
    logger.info(f"Fetching country info.")
    try:
        response = scraper.scrape_website(CATEGORIES_URL)
        data = response.get('categories')
        return data # tr için 46 döner bu servisten
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return []


def get_unique_tournaments(country_id: int) -> list:
    logger.info(f"Fetching tournaments for the country specified.")
    try:
        response = scraper.scrape_website(UNIQUE_TOURNAMENTS_URL.format(country_id))
        data = response.get('groups')[0].get('uniqueTournaments')
        return data
    except Exception as e:
        logger.error(f"Error fetching tournaments by country: {e}")
        return []


def get_featured_events(tournament_id: int) -> list:
    logger.info(f"Fetching featured events for the tournament id specified.")
    try:
        response = scraper.scrape_website(SEASONS_URL.format(tournament_id))
        data = response.get('featuredEvents')[0]
        return data
    except Exception as e:
        logger.error(f"Error fetching featured events by country: {e}")
        return []


def get_seasons(unique_tournament_id: int) -> list:
    logger.info(f"Fetching seasons for country id.")
    try:
        response = scraper.scrape_website(SEASONS_URL.format(unique_tournament_id))
        if response.get('seasons'):
            data = response.get('seasons')
            return data
        else:
            return []
    except Exception as e:
        logger.error(f"Error fetching seasons by country: {e}")
        return []



def get_round_matches(tournament_id: int, season_id: int, week: int) -> list:
    """
    Belirli bir lig, sezon ve haftadaki maçları getirir.

    Args:
        tournament_id (int): Ligin ID'si.
        season_id (int): Sezonun ID'si.
        week (int): Hafta sayısı.

    Returns:
        list: Maçların listesi.
    """

    logger.info(f"Fetching matches for tournament_id: {tournament_id}, season_id: {season_id}, week: {week}")
    try:
        response = scraper.scrape_website(ROUNDS_URL.format(tournament_id, season_id, week))
        return response.get('events')
    except Exception as e:
        logger.error(f"Error fetching matches for tournament {tournament_id}, season {season_id}, week {week}: {e}")
        return []


def get_rounds_unique_tournament(country_id: int, season_id: int, page: int = 0) -> list:
    """
    Finlandiya gibi farklı liglerin maç sonuçlarını döner.

    Args:
        country_id (int): Ülke Kodu.
        season_id (int): Sezon Kodu.
        Page (int): Sayfa Numarası.

    Returns:
        list: Maçların listesi
    """
    more_events = []
    logger.info(f"Fetching matches for country_id: {country_id}, season_id: {season_id}, page: {page}")
    try:
        response = scraper.scrape_website(UNIQUE_ROUND_URL.format(country_id, season_id, page))
        if response.get('hasNextPage'):
            more_events = get_rounds_unique_tournament(country_id, season_id, page+1)
        return more_events + response.get('events')
    except Exception as e:
        logger.error(f"Error fetching matches for country {country_id}, season {season_id}, page {page}: {e}")
        return []


def get_top_tournaments(country_alpha2: str) -> list:
    """
    En ünlü liglerin bilgilerini getirir..

    Args:
        country_alpha2 (str): Ülke kodu.

    Returns:
        list: Ülkeler ve ligler listesi
    """

    logger.info(f"Fetching tournaments for country: {country_alpha2}")
    try:
        response = scraper.scrape_website(TOP_TOURNAMENTS_URL.format(country_alpha2))
        data = pd.DataFrame(response.get('uniqueTournaments'))
        return data # bu pandas frame döndürsün
    except Exception as e:
        logger.error(f"Error fetching tournaments for {country_alpha2}: {e}")
        return []


def get_match_events(match_id: int) -> list:
    """
    Belirli bir maçın olaylarını (incidents) getirir.

    Args:
        match_id (int): Maçın ID'si.

    Returns:
        list: Maç olaylarının listesi.
    """
    logger.info(f"Fetching events for match_id: {match_id}")
    try:
        response = scraper.scrape_website(INCIDENTS_URL.format(match_id))
        return response
    except Exception as e:
        logger.error(f"Error fetching events for match {match_id}: {e}")
        return []


def get_match_statistics(match_id: int) -> list:
    """
    Belirli bir maçın istatistiklerini getirir.

    Args:
        match_id (int): Maçın ID'si.

    Returns:
        list: Maç istatistiklerinin listesi.
    """
    logger.info(f"Fetching statistics for match_id: {match_id}")
    try:
        response = scraper.scrape_website(STATISTICS_URL.format(match_id))
        return response
    except Exception as e:
        logger.error(f"Error fetching statistics for match {match_id}: {e}")
        return []
    
def get_team_statistics(team_id: int, unique_tournament_id: int, season_id: int) -> list:
    """
    Belirli bir takımın sezonluk istatistiklerini getirir.

    Args:
        team_id (int): Takımın ID'si.
        tournament_id (int): Ligin ID'si.
        season_id (int): Sezonun ID'si.

    Returns:
        list: Takım istatistiklerinin listesi.
    """
    logger.info(f"Fetching statistics for team_id: {team_id}, tournament_id: {unique_tournament_id}, season_id: {season_id}")
    try:
        response = scraper.scrape_website(TEAM_STATS_URL.format(team_id, unique_tournament_id, season_id))
        return response
    except Exception as e:
        logger.error(f"Error fetching statistics for team {team_id}, tournament {unique_tournament_id}, season {season_id}: {e}")
        return []


def get_match_graph(match_id: int) -> dict:
    """
    Belirli bir maçın momentum grafiğini getirir.

    Args:
        match_id (int): Maçın ID'si.

    Returns:
        dict: Maç momentum grafiği verisi.
    """
    logger.info(f"Fetching momentum graph for match_id: {match_id}")

    try:
        response = scraper.scrape_website(MOMENTUM_URL.format(match_id))
        return response
    except Exception as e:
        logger.error(f"Error fetching momentum graph for match {match_id}: {e}")
        return {}


