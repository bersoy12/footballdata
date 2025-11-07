--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: football_passing_network_action; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.football_passing_network_action (
    incident_id bigint,
    player_id bigint,
    player_name character varying(100),
    event_type character varying(50),
    is_assist boolean,
    body_part character varying(50),
    goal_type character varying(50)
);


ALTER TABLE public.football_passing_network_action OWNER TO postgres;

--
-- Name: incident; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.incident (
    match_id bigint,
    incident_id double precision,
    "time" integer,
    incident_type character varying(50),
    incident_class character varying(50),
    reason character varying(255),
    text_ character varying(20),
    player_in_name character varying(255),
    player_in_id double precision,
    player_out_name character varying(255),
    player_out_id double precision,
    injury character varying,
    scorer_name character varying(100),
    scorer_id double precision,
    assist1_name character varying(100),
    assist1_id double precision,
    rescinded character varying(50),
    card_player_name character varying(100),
    card_player_id double precision,
    from_ character varying(50),
    added_time double precision,
    home_score double precision,
    away_score double precision,
    length_ double precision,
    confirmed character varying(50),
    var_player character varying(255),
    passing_network json
);


ALTER TABLE public.incident OWNER TO postgres;

--
-- Name: match; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.match (
    match_id bigint,
    tournament_id integer,
    unique_tournament_id integer,
    tournament_name character varying(255),
    country_name character varying(255),
    alpha2 character varying(10),
    sport character varying(50),
    season_year character varying(50),
    season_id integer,
    round integer,
    start_timestamp bigint,
    slug character varying(255),
    status_code integer,
    status_type character varying(50),
    winner_code integer,
    home_team_name character varying(255),
    home_team_id integer,
    away_team_name character varying(255),
    away_team_id integer,
    home_score_period1 integer,
    home_score_period2 integer,
    home_score_normaltime integer,
    away_score_period1 integer,
    away_score_period2 integer,
    away_score_normaltime integer,
    time_injury_time1 double precision,
    time_injury_time2 double precision
);


ALTER TABLE public.match OWNER TO postgres;

--
-- Name: country; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country (
    country_id bigint,
    country_name character varying(255),
    country_alpha2 character varying(50),
    -- tournament_id integer,
    -- unique_tournament_id integer,
    -- tournament_name character varying(255),
    -- season_id integer,
    -- season_year character varying(50)
);


ALTER TABLE public.country OWNER TO postgres;

--
-- Name: momentum; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.momentum (
    match_id bigint,
    minute numeric,
    value integer
);


ALTER TABLE public.momentum OWNER TO postgres;

--
-- Name: season; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.season (
    season_id integer,
    tournament_id integer,
    name character varying(255),
    year character varying(10)
);


ALTER TABLE public.season OWNER TO postgres;

--
-- Name: statistic; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.statistic (
    match_id bigint,
    period character varying(10),
    group_name character varying(255),
    statistics_name character varying(255),
    value_type character varying(50),
    key character varying(255),
    statistics_type character varying(50),
    away_value character varying(255),
    home_value character varying(255)
);


ALTER TABLE public.statistic OWNER TO postgres;

--
-- Name: team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team (
    id integer,
    name character varying(255),
    slug character varying(255),
    short_name character varying(50),
    country_alpha3 character varying(3)
);


ALTER TABLE public.team OWNER TO postgres;

--
-- Name: tournament; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tournament (
    country_id integer NOT NULL,
    tournament_id integer NOT NULL,
    tournament_name character varying(255),
    sport character varying(50)
);


ALTER TABLE public.tournament OWNER TO postgres;



CREATE TABLE public.team_statistics_overall (
    id bigint PRIMARY KEY,
    team_id integer,
    unique_tournament_id integer,
    tournament_id integer,
    season_id integer,
    goals_scored integer,
    goals_conceded integer,
    own_goals integer,
    assists integer,
    shots integer,
    penalty_goals integer,
    penalties_taken integer,
    free_kick_goals integer,
    free_kick_shots integer,
    goals_from_inside_the_box integer,
    goals_from_outside_the_box integer,
    shots_from_inside_the_box integer,
    shots_from_outside_the_box integer,
    headed_goals integer,
    left_foot_goals integer,
    right_foot_goals integer,
    big_chances integer,
    big_chances_created integer,
    big_chances_missed integer,
    shots_on_target integer,
    shots_off_target integer,
    blocked_scoring_attempt integer,
    successful_dribbles integer,
    dribble_attempts integer,
    corners integer,
    hit_woodwork integer,
    fast_breaks integer,
    fast_break_goals integer,
    fast_break_shots integer,
    average_ball_possession double precision,
    total_passes integer,
    accurate_passes integer,
    accurate_passes_percentage double precision,
    total_own_half_passes integer,
    accurate_own_half_passes integer,
    accurate_own_half_passes_percentage double precision,
    total_opposition_half_passes integer,
    accurate_opposition_half_passes integer,
    accurate_opposition_half_passes_percentage double precision,
    total_long_balls integer,
    accurate_long_balls integer,
    accurate_long_balls_percentage double precision,
    total_crosses integer,
    accurate_crosses integer,
    accurate_crosses_percentage double precision,
    clean_sheets integer,
    tackles integer,
    interceptions integer,
    saves integer,
    errors_leading_to_goal integer,
    errors_leading_to_shot integer,
    penalties_committed integer,
    penalty_goals_conceded integer,
    clearances integer,
    clearances_off_line integer,
    last_man_tackles integer,
    total_duels integer,
    duels_won integer,
    duels_won_percentage double precision,
    total_ground_duels integer,
    ground_duels_won integer,
    ground_duels_won_percentage double precision,
    total_aerial_duels integer,
    aerial_duels_won integer,
    aerial_duels_won_percentage double precision,
    possession_lost integer,
    offsides integer,
    fouls integer,
    yellow_cards integer,
    yellow_red_cards integer,
    red_cards integer,
    avg_rating double precision,
    accurate_final_third_passes_against integer,
    accurate_opposition_half_passes_against integer,
    accurate_own_half_passes_against integer,
    accurate_passes_against integer,
    big_chances_against integer,
    big_chances_created_against integer,
    big_chances_missed_against integer,
    clearances_against integer,
    corners_against integer,
    crosses_successful_against integer,
    crosses_total_against integer,
    dribble_attempts_total_against integer,
    dribble_attempts_won_against integer,
    errors_leading_to_goal_against integer,
    errors_leading_to_shot_against integer,
    hit_woodwork_against integer,
    interceptions_against integer,
    key_passes_against integer,
    long_balls_successful_against integer,
    long_balls_total_against integer,
    offsides_against integer,
    red_cards_against integer,
    shots_against integer,
    shots_blocked_against integer,
    shots_from_inside_the_box_against integer,
    shots_from_outside_the_box_against integer,
    shots_off_target_against integer,
    shots_on_target_against integer,
    blocked_scoring_attempt_against integer,
    tackles_against integer,
    total_final_third_passes_against integer,
    opposition_half_passes_total_against integer,
    own_half_passes_total_against integer,
    total_passes_against integer,
    yellow_cards_against integer,
    throw_ins integer,
    goal_kicks integer,
    ball_recovery integer,
    free_kicks integer,
    number_of_sprints integer,
    matches integer,
    awarded_matches integer
);
-- -- Indexes for common filters:
-- CREATE INDEX idx_team_statistics_team_id ON public.team_statistics_overall(team_id);
-- CREATE INDEX idx_team_statistics_season ON public.team_statistics_overall(season_id);
-- CREATE INDEX idx_team_statistics_tournament ON public.team_statistics_overall(unique_tournament_id);
ALTER TABLE public.team_statistics_overall OWNER TO postgres;

--
-- Name: match match_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.match
    ADD CONSTRAINT match_id_unique UNIQUE (match_id);


--
-- Name: tournament tournament_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tournament
    ADD CONSTRAINT tournament_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

