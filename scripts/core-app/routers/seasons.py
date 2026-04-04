from fastapi import APIRouter, Body, Query
from typing import List
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from itertools import chain

from services.season_service import (
    sezonlari_isle
)


router = APIRouter()


@router.get("/sezonlari-getir")
def sezonlari_getir_endpoint(
    unique_tournament_id: int,
    insert_to_db: bool = False,
):
    return sezonlari_isle(unique_tournament_id, insert_to_db)