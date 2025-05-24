CREATE TABLE IF NOT EXISTS tournament (
    id INTEGER PRIMARY KEY, --- turnuva id 52 süper lig tr
    name VARCHAR(255) --- turnuva adı
);

CREATE TABLE IF NOT EXISTS team (
    id INTEGER, -- PRIMARY KEY
    name VARCHAR(255),
    slug VARCHAR(255),
    short_name VARCHAR(50),
    country_alpha3 VARCHAR(3)
);

CREATE TABLE IF NOT EXISTS season (
    season_id INTEGER, -- PRIMARY KEY
    tournament_id INTEGER,
    name VARCHAR(255),
    year VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS match (
    match_id BIGINT, -- PRIMARY KEY
    tournament_id INTEGER, --- REFERENCES tournament(tournament_id)
    season_id INTEGER,
    round INTEGER,
    start_timestamp BIGINT,
    slug VARCHAR(255),
    status_code INTEGER,
    status_type VARCHAR(50),
    winner_code INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_score_period1 INTEGER,
    home_score_period2 INTEGER,
    home_score_normaltime INTEGER,
    away_score_period1 INTEGER,
    away_score_period2 INTEGER,
    away_score_normaltime INTEGER,
    time_injury_time1 INTEGER,
    time_injury_time2 INTEGER
);

CREATE TABLE IF NOT EXISTS incident (
    match_id BIGINT, --- REFERENCES match(match_id)
    incident_id BIGINT,
    time INTEGER,
    incident_type VARCHAR(50),
    incident_class VARCHAR(50),
    reason VARCHAR(255),
    text_ VARCHAR(20),
    player_in_name VARCHAR(255),
    player_in_id BIGINT,
    player_out_name VARCHAR(255),
    player_out_id BIGINT,
    injury BOOLEAN,
    scorer_name VARCHAR(100),
    scorer_id BIGINT,
    assist1_name VARCHAR(100),
    assist1_id BIGINT,
    rescinded VARCHAR(50),
    card_player_name VARCHAR(100),
    card_player_id BIGINT,
    from_ VARCHAR(50),
    added_time INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    length_ INTEGER,
    confirmed VARCHAR(50),
    var_player VARCHAR(255),
    passing_network JSON
);

CREATE TABLE IF NOT EXISTS football_passing_network_action (
    incident_id BIGINT,
    player_id BIGINT,
    player_name VARCHAR(100),
    event_type VARCHAR(50),
    is_assist BOOLEAN,
    body_part VARCHAR(50),
    goal_type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS statistic (
    id SERIAL PRIMARY KEY,
    match_id BIGINT, -- REFERENCES match(match_id)
    period VARCHAR(10),
    group_name VARCHAR(255),
    statistic_item_name VARCHAR(255),
    value_type VARCHAR(50),
    home_value NUMERIC,
    away_value NUMERIC,
    key VARCHAR(255),
    statistics_type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS match_momentum (
    match_id BIGINT, -- REFERENCES match(match_id)
    minute NUMERIC,
    value INTEGER
);