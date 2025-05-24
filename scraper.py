from cloudflarescraper import CloudflareScraper
import pandas as pd
import os
import json
from dotenv import load_dotenv

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
    try:
        response = scraper.scrape_website(TOURNAMENTS_URL.format(country_alpha2))
        data = pd.DataFrame(response.get('uniqueTournaments'))
        return data # bu pandas frame döndürsün
    except Exception as e:
        print(f"Turnuvalar servisinde hata oluştu: {e}")
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
    try:
        response = scraper.scrape_website(ROUNDS_URL.format(tournament_id, season_id, week))
        # print(response.get('events'))
        return response.get('events')
    except Exception as e:
        print(f"Haftalık maçlar servisinde hata oluştu: {e}")
        return []


def get_match_events(match_id: int) -> list:
    """
    Belirli bir maçın olaylarını (incidents) getirir.

    Args:
        match_id (int): Maçın ID'si.

    Returns:
        list: Maç olaylarının listesi.
    """
    print(f"{match_id} maçı olayları alınıyor...")
    try:
        response = scraper.scrape_website(INCIDENTS_URL.format(match_id))
        return response
    except Exception as e:
        print(f"Olaylar servisinde hata oluştu: {e}")
        return []


def get_match_statistics(match_id: int) -> list:
    """
    Belirli bir maçın istatistiklerini getirir.

    Args:
        match_id (int): Maçın ID'si.

    Returns:
        list: Maç istatistiklerinin listesi.
    """
    print(f"{match_id} maçı istatistikleri alınıyor...")
    try:
        response = scraper.scrape_website(STATISTICS_URL.format(match_id))
        return response
    except Exception as e:
        print(f"İstatistikler servisinde hata oluştu: {e}")
        return []


def get_match_graph(match_id: int) -> dict:
    """
    Belirli bir maçın momentum grafiğini getirir.

    Args:
        match_id (int): Maçın ID'si.

    Returns:
        dict: Maç momentum grafiği verisi.
    """
    print(f"{match_id} maç momentum grafiği alınıyor...")
    try:
        response = scraper.scrape_website(MOMENTUM_URL.format(match_id))
        return response
    except Exception as e:
        print(f"Grafik servisinde hata oluştu: {e}")
        return {}


