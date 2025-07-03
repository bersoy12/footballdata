from sqlalchemy import Column, BigInteger, Integer, String, Double, DOUBLE_PRECISION
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Country(Base):
    __tablename__ = "country"

    country_id = Column(BigInteger, primary_key=True)
    country_name = Column(String(255))
    country_aplha2 = Column(String(50))


class Tournament(Base):
    __tablename__ = "tournament"

    tournament_id = Column(BigInteger, primary_key=True)
    tournament_name = Column(String(255))
    sport = Column(String(255))
    season_id = Column(BigInteger)
    season_year = Column(String(255))

