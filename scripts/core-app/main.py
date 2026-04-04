import logging
from fastapi import FastAPI, Body
from cloudflarescraper import CloudflareScraper

from routers import teams, pipeline, matches, statistics, database, tournaments, reports, seasons

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})


app.include_router(tournaments.router, tags=["Turnuvalar"])
app.include_router(seasons.router,     tags=["Sezonlar"])
app.include_router(teams.router,       tags=["Takımlar"])
app.include_router(matches.router,     tags=["Maçlar"])
app.include_router(statistics.router,  tags=["İstatistik"])
app.include_router(database.router,    tags=["Veritabanı"])
app.include_router(reports.router,     tags=["Raporlar"])
app.include_router(pipeline.router,    tags=["Pipeline"])