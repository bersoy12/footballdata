from cloudflarescraper import CloudflareScraper
import pandas as pd
import os
import json
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

TOURNAMENTS_URL = os.getenv('TOURNAMENTS_URL')
STANDINGS_URL = os.getenv('STANDINGS_URL')
ROUNDS_URL = os.getenv('ROUNDS_URL')
INCIDENTS_URL = os.getenv('INCIDENTS_URL')
STATISTICS_URL = os.getenv('STATISTICS_URL')
MOMENTUM_URL = os.getenv('MOMENTUM_URL')

scraper = CloudflareScraper()
    

# def get_tournaments(country_alpha2: str = "TR")
def get_tournaments(country_alpha2: str) -> list:
    """
    Belirli bir maçın olaylarını (incidents) getirir.

    Args:
        match_id (int): Maçın ID'si.

    Returns:
        list: Maç olaylarının listesi.
    """

    logger.info(f"Fetching tournaments for country: {country_alpha2}")
    try:
        response = scraper.scrape_website(TOURNAMENTS_URL.format(country_alpha2))
        data = pd.DataFrame(response.get('uniqueTournaments'))
        return data # bu pandas frame döndürsün
    except Exception as e:
        logger.error(f"Error fetching tournaments for {country_alpha2}: {e}")
        return []


def get_season(country_alpha2: str) -> list:
    pass

# def get_round_matches(league_id: int = 52, season_id: int = 63814, week: int = 1)
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


