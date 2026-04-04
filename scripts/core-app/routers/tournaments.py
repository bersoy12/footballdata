from fastapi import APIRouter
from services.tournament_service import (
    ulke_bilgisi_getir,
    turnuvalari_getir,
    unique_tournaments_getir,
)
import datetime
datetime.datetime.now().strftime("%Y-%m-%d")

router = APIRouter()


@router.get("/ulke-bilgisi-getir")
def ulke_bilgisi_getir_endpoint():
    return ulke_bilgisi_getir()


@router.get("/turnuvalari-getir")
def turnuvalari_getir_endpoint(country_id: int, date: str = datetime.datetime.now().strftime("%Y-%m-%d")):
    return turnuvalari_getir(country_id, date)


@router.get("/unique-tournaments-getir")
def unique_tournaments_endpoint(country_id: int):
    return unique_tournaments_getir(country_id)
