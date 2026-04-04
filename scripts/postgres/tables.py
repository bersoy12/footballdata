from sqlalchemy import (
    Column, BigInteger, Integer, SmallInteger, String, ForeignKey,
    Boolean, Numeric, Float, Text, Date, JSON
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "country"

    country_id = Column(BigInteger, primary_key=True)
    country_name = Column(String(255))
    country_alpha2 = Column(String(50))


class Tournament(Base):
    __tablename__ = "tournament"

    country_id = Column(Integer, nullable=False)
    tournament_id = Column(Integer, nullable=False, primary_key=True)
    tournament_name = Column(String(255))
    sport = Column(String(50))
    season_id = Column(Float)
    season_year = Column(String(50))
    season_name = Column(String(255))
    round_info = Column(Float)
    gender = Column(String(50))
    date = Column(Date)


class UniqueTournament(Base):
    __tablename__ = "unique_tournament"

    unique_tournament_id = Column(Integer, primary_key=True)
    country_id = Column(Integer)
    tournament_name = Column(String(255))
    sport_id = Column(Integer)
    sport_name = Column(String(50))


class Season(Base):
    __tablename__ = "season"

    season_id = Column(Integer, primary_key=True)
    unique_tournament_id = Column(Integer)
    name = Column(String(255))
    year = Column(String(10))


class Team(Base):
    __tablename__ = "team"

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String(255))
    name_code = Column(String(50))
    sport_id = Column(Integer)
    sport_name = Column(String(50))
    disabled = Column(Boolean)
    national = Column(Boolean)
    country_id = Column(Integer)
    tournament_id = Column(Integer)
    unique_tournament_id = Column(Integer)
    team_colors_primary = Column(String(50))
    team_colors_secondary = Column(String(50))


class Match(Base):
    __tablename__ = "match"

    match_id = Column(BigInteger, primary_key=True)
    tournament_id = Column(Integer)
    unique_tournament_id = Column(Integer)
    country_id = Column(Integer)
    season_id = Column(Integer)
    round = Column(Integer)
    start_timestamp = Column(BigInteger)
    slug = Column(String(255))
    status_code = Column(Integer)
    status_type = Column(String(50))
    winner_code = Column(Integer)
    home_team_name = Column(String(255))
    home_team_id = Column(Integer)
    away_team_name = Column(String(255))
    away_team_id = Column(Integer)
    home_score_period1 = Column(Integer)
    home_score_period2 = Column(Integer)
    home_score_normaltime = Column(Integer)
    away_score_period1 = Column(Integer)
    away_score_period2 = Column(Integer)
    away_score_normaltime = Column(Integer)
    time_injury_time1 = Column(Float)
    time_injury_time2 = Column(Float)


class Incident(Base):
    __tablename__ = "incident"

    match_id = Column(BigInteger)
    incident_id = Column(Float)
    time = Column(Integer)
    incident_type = Column(String(50))
    incident_class = Column(String(50))
    reason = Column(String(255))
    text_ = Column(String(20))
    player_in_name = Column(String(255))
    player_in_id = Column(Float)
    player_out_name = Column(String(255))
    player_out_id = Column(Float)
    injury = Column(Text)
    scorer_name = Column(String(100))
    scorer_id = Column(Float)
    assist1_name = Column(String(100))
    assist1_id = Column(Float)
    rescinded = Column(String(50))
    card_player_name = Column(String(100))
    card_player_id = Column(Float)
    from_ = Column(String(50))
    added_time = Column(Float)
    home_score = Column(Float)
    away_score = Column(Float)
    length_ = Column(Float)
    confirmed = Column(String(50))
    var_player = Column(String(255))
    passing_network = Column(JSON)


class FootballPassingNetworkAction(Base):
    __tablename__ = "football_passing_network_action"

    incident_id = Column(BigInteger)
    player_id = Column(BigInteger)
    player_name = Column(String(100))
    event_type = Column(String(50))
    is_assist = Column(Boolean)
    body_part = Column(String(50))
    goal_type = Column(String(50))


class Momentum(Base):
    __tablename__ = "momentum"

    match_id = Column(BigInteger)
    minute = Column(Numeric)
    value = Column(Integer)


class Statistic(Base):
    __tablename__ = "statistic"

    match_id = Column(BigInteger)
    period = Column(String(10))
    group_name = Column(String(255))
    statistics_name = Column(String(255))
    value_type = Column(String(50))
    key = Column(String(255))
    statistics_type = Column(String(50))
    away_value = Column(String(255))
    home_value = Column(String(255))


class TeamStatisticsOverall(Base):
    __tablename__ = "team_statistics_overall"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer)
    unique_tournament_id = Column(Integer)
    tournament_id = Column(Integer)
    season_id = Column(Integer)
    goals_scored = Column(Integer)
    goals_conceded = Column(Integer)
    own_goals = Column(Integer)
    assists = Column(Integer)
    shots = Column(Integer)
    penalty_goals = Column(Integer)
    penalties_taken = Column(Integer)
    free_kick_goals = Column(Integer)
    free_kick_shots = Column(Integer)
    goals_from_inside_the_box = Column(Integer)
    goals_from_outside_the_box = Column(Integer)
    shots_from_inside_the_box = Column(Integer)
    shots_from_outside_the_box = Column(Integer)
    headed_goals = Column(Integer)
    left_foot_goals = Column(Integer)
    right_foot_goals = Column(Integer)
    big_chances = Column(Integer)
    big_chances_created = Column(Integer)
    big_chances_missed = Column(Integer)
    shots_on_target = Column(Integer)
    shots_off_target = Column(Integer)
    blocked_scoring_attempt = Column(Integer)
    successful_dribbles = Column(Integer)
    dribble_attempts = Column(Integer)
    corners = Column(Integer)
    hit_woodwork = Column(Integer)
    fast_breaks = Column(Integer)
    fast_break_goals = Column(Integer)
    fast_break_shots = Column(Integer)
    average_ball_possession = Column(Float)
    total_passes = Column(Integer)
    accurate_passes = Column(Integer)
    accurate_passes_percentage = Column(Float)
    total_own_half_passes = Column(Integer)
    accurate_own_half_passes = Column(Integer)
    accurate_own_half_passes_percentage = Column(Float)
    total_opposition_half_passes = Column(Integer)
    accurate_opposition_half_passes = Column(Integer)
    accurate_opposition_half_passes_percentage = Column(Float)
    total_long_balls = Column(Integer)
    accurate_long_balls = Column(Integer)
    accurate_long_balls_percentage = Column(Float)
    total_crosses = Column(Integer)
    accurate_crosses = Column(Integer)
    accurate_crosses_percentage = Column(Float)
    clean_sheets = Column(Integer)
    tackles = Column(Integer)
    interceptions = Column(Integer)
    saves = Column(Integer)
    errors_leading_to_goal = Column(Integer)
    errors_leading_to_shot = Column(Integer)
    penalties_committed = Column(Integer)
    penalty_goals_conceded = Column(Integer)
    clearances = Column(Integer)
    clearances_off_line = Column(Integer)
    last_man_tackles = Column(Integer)
    total_duels = Column(Integer)
    duels_won = Column(Integer)
    duels_won_percentage = Column(Float)
    total_ground_duels = Column(Integer)
    ground_duels_won = Column(Integer)
    ground_duels_won_percentage = Column(Float)
    total_aerial_duels = Column(Integer)
    aerial_duels_won = Column(Integer)
    aerial_duels_won_percentage = Column(Float)
    possession_lost = Column(Integer)
    offsides = Column(Integer)
    fouls = Column(Integer)
    yellow_cards = Column(Integer)
    yellow_red_cards = Column(Integer)
    red_cards = Column(Integer)
    avg_rating = Column(Float)
    accurate_final_third_passes_against = Column(Integer)
    accurate_opposition_half_passes_against = Column(Integer)
    accurate_own_half_passes_against = Column(Integer)
    accurate_passes_against = Column(Integer)
    big_chances_against = Column(Integer)
    big_chances_created_against = Column(Integer)
    big_chances_missed_against = Column(Integer)
    clearances_against = Column(Integer)
    corners_against = Column(Integer)
    crosses_successful_against = Column(Integer)
    crosses_total_against = Column(Integer)
    dribble_attempts_total_against = Column(Integer)
    dribble_attempts_won_against = Column(Integer)
    errors_leading_to_goal_against = Column(Integer)
    errors_leading_to_shot_against = Column(Integer)
    hit_woodwork_against = Column(Integer)
    interceptions_against = Column(Integer)
    key_passes_against = Column(Integer)
    long_balls_successful_against = Column(Integer)
    long_balls_total_against = Column(Integer)
    offsides_against = Column(Integer)
    red_cards_against = Column(Integer)
    shots_against = Column(Integer)
    shots_blocked_against = Column(Integer)
    shots_from_inside_the_box_against = Column(Integer)
    shots_from_outside_the_box_against = Column(Integer)
    shots_off_target_against = Column(Integer)
    shots_on_target_against = Column(Integer)
    blocked_scoring_attempt_against = Column(Integer)
    tackles_against = Column(Integer)
    total_final_third_passes_against = Column(Integer)
    opposition_half_passes_total_against = Column(Integer)
    own_half_passes_total_against = Column(Integer)
    total_passes_against = Column(Integer)
    yellow_cards_against = Column(Integer)
    throw_ins = Column(Integer)
    goal_kicks = Column(Integer)
    ball_recovery = Column(Integer)
    free_kicks = Column(Integer)
    number_of_sprints = Column(Integer)
    matches = Column(Integer)
    awarded_matches = Column(Integer)