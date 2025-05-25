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
    season_id integer,
    round integer,
    start_timestamp bigint,
    slug character varying(255),
    status_code integer,
    status_type character varying(50),
    winner_code integer,
    home_team_id integer,
    away_team_id integer,
    home_score_period1 integer,
    home_score_period2 integer,
    home_score_normaltime integer,
    away_score_period1 integer,
    away_score_period2 integer,
    away_score_normaltime integer,
    time_injury_time1 integer,
    time_injury_time2 integer
);


ALTER TABLE public.match OWNER TO postgres;

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
    id integer NOT NULL,
    name character varying(255)
);


ALTER TABLE public.tournament OWNER TO postgres;

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

