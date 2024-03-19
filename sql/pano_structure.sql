--
-- PostgreSQL database dump
--

-- Dumped from database version 12.17 (Ubuntu 12.17-1.pgdg20.04+1)
-- Dumped by pg_dump version 12.17 (Ubuntu 12.17-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

-- CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

-- COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

-- COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: rand(); Type: FUNCTION; Schema: public; Owner: cms
--

CREATE FUNCTION public.rand() RETURNS double precision
   LANGUAGE sql
   AS $$SELECT random();$$;


-- ALTER FUNCTION public.rand() OWNER TO cms;

--
-- Name: substring_index(text, text, integer); Type: FUNCTION; Schema: public; Owner: cms
--

CREATE FUNCTION public.substring_index(text, text, integer) RETURNS text
   LANGUAGE sql
   AS $_$SELECT array_to_string((string_to_array($1, $2)) [1:$3], $2);$_$;


-- ALTER FUNCTION public.substring_index(text, text, integer) OWNER TO cms;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cache_container; Type: TABLE; Schema: public; Owner: cms
--

CREATE TABLE IF NOT EXISTS public.cache_container (
    cid character varying(255) DEFAULT ''::character varying NOT NULL,
    data bytea,
    expire integer DEFAULT 0 NOT NULL,
    created numeric(14,3) DEFAULT 0 NOT NULL,
    serialized smallint DEFAULT 0 NOT NULL,
    tags text,
    checksum character varying(255) NOT NULL
);


-- ALTER TABLE public.cache_container OWNER TO cms;

--
-- Name: TABLE cache_container; Type: COMMENT; Schema: public; Owner: cms
--

-- COMMENT ON TABLE public.cache_container IS 'Storage for the cache API.';


--
-- Name: COLUMN cache_container.cid; Type: COMMENT; Schema: public; Owner: cms
--

COMMENT ON COLUMN public.cache_container.cid IS 'Primary Key: Unique cache ID.';


--
-- Name: COLUMN cache_container.data; Type: COMMENT; Schema: public; Owner: cms
--

COMMENT ON COLUMN public.cache_container.data IS 'A collection of data to cache.';


--
-- Name: COLUMN cache_container.expire; Type: COMMENT; Schema: public; Owner: cms
--

COMMENT ON COLUMN public.cache_container.expire IS 'A Unix timestamp indicating when the cache entry should expire, or -1 for never.';


--
-- Name: COLUMN cache_container.created; Type: COMMENT; Schema: public; Owner: cms
--

COMMENT ON COLUMN public.cache_container.created IS 'A timestamp with millisecond precision indicating when the cache entry was created.';


--
-- Name: COLUMN cache_container.serialized; Type: COMMENT; Schema: public; Owner: cms
--

COMMENT ON COLUMN public.cache_container.serialized IS 'A flag to indicate whether content is serialized (1) or not (0).';


--
-- Name: COLUMN cache_container.tags; Type: COMMENT; Schema: public; Owner: cms
--

COMMENT ON COLUMN public.cache_container.tags IS 'Space-separated list of cache tags for this entry.';


--
-- Name: COLUMN cache_container.checksum; Type: COMMENT; Schema: public; Owner: cms
--

COMMENT ON COLUMN public.cache_container.checksum IS 'The tag invalidation checksum when this entry was saved.';


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: panorama
--

CREATE TABLE IF NOT EXISTS public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


-- ALTER TABLE public.django_content_type OWNER TO panorama;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: panorama
--

CREATE SEQUENCE IF NOT EXISTS public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER TABLE public.django_content_type_id_seq OWNER TO panorama;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: panorama
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: panorama
--

CREATE TABLE IF NOT EXISTS public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


-- ALTER TABLE public.django_migrations OWNER TO panorama;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: panorama
--

CREATE SEQUENCE IF NOT EXISTS public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER TABLE public.django_migrations_id_seq OWNER TO panorama;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: panorama
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: panorama
--

CREATE TABLE IF NOT EXISTS public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


-- ALTER TABLE public.django_session OWNER TO panorama;

--
-- Name: panoramas_panorama; Type: TABLE; Schema: public; Owner: panorama
--

CREATE TABLE IF NOT EXISTS public.panoramas_panorama (
    id integer NOT NULL,
    pano_id character varying(37) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    filename character varying(255) NOT NULL,
    path character varying(400) NOT NULL,
    geolocation extensions.geometry(PointZ,4326) NOT NULL,
    roll double precision NOT NULL,
    pitch double precision NOT NULL,
    heading double precision NOT NULL,
    _geolocation_2d extensions.geometry(Point,4326),
    status character varying(100) NOT NULL,
    status_changed timestamp with time zone NOT NULL,
    mission_type text NOT NULL,
    _geolocation_2d_rd extensions.geometry(Point,28992),
    mission_year integer NOT NULL,
    surface_type character varying(1) NOT NULL,
    mission_distance integer NOT NULL,
    tags character varying(32)[] NOT NULL
);


-- ALTER TABLE public.panoramas_panorama OWNER TO panorama;

--
-- Name: panoramas_adjacencies_new; Type: VIEW; Schema: public; Owner: panorama
--

CREATE VIEW public.panoramas_adjacencies_new AS
 SELECT subquery1.id,
    subquery1.from_pano_id,
    subquery1.to_pano_id AS pano_id,
    subquery1.to_filename AS filename,
    subquery1.to_path AS path,
    subquery1.to_surface_type AS surface_type,
    subquery1.to_mission_type AS mission_type,
    subquery1.to_mission_distance AS mission_distance,
    subquery1.to_mission_year AS mission_year,
    subquery1.to_tags AS tags,
    subquery1.to_timestamp AS "timestamp",
    subquery1.to_status AS status,
    subquery1.to_status_changed AS status_changed,
    subquery1.relative_distance,
    subquery1.relative_heading,
    degrees(atan2(subquery1.relative_elevation, subquery1.relative_distance)) AS relative_pitch,
    subquery1.relative_elevation,
    subquery1.from_geolocation_2d_rd,
    subquery1.to_geolocation_2d_rd AS _geolocation_2d_rd,
    subquery1.to_geolocation_2d AS _geolocation_2d,
    subquery1.to_geolocation AS geolocation
   FROM ( SELECT ((from_pano.id || '-'::text) || to_pano.id) AS id,
            from_pano.pano_id AS from_pano_id,
            to_pano.pano_id AS to_pano_id,
            to_pano.filename AS to_filename,
            to_pano.path AS to_path,
            to_pano.surface_type AS to_surface_type,
            to_pano.mission_type AS to_mission_type,
            to_pano.mission_distance AS to_mission_distance,
            to_pano.mission_year AS to_mission_year,
            to_pano.tags AS to_tags,
            to_pano."timestamp" AS to_timestamp,
            to_pano.status AS to_status,
            to_pano.status_changed AS to_status_changed,
            extensions.st_distance(extensions.geography(to_pano.geolocation), extensions.geography(from_pano.geolocation)) AS relative_distance,
            degrees(extensions.st_azimuth(extensions.geography(from_pano.geolocation), extensions.geography(to_pano.geolocation))) AS relative_heading,
            (extensions.st_z(to_pano.geolocation) - extensions.st_z(from_pano.geolocation)) AS relative_elevation,
            from_pano._geolocation_2d_rd AS from_geolocation_2d_rd,
            to_pano._geolocation_2d_rd AS to_geolocation_2d_rd,
            to_pano._geolocation_2d AS to_geolocation_2d,
            to_pano.geolocation AS to_geolocation
           FROM public.panoramas_panorama from_pano,
            public.panoramas_panorama to_pano
          WHERE ((to_pano.status)::text = 'done'::text)) subquery1;


-- ALTER TABLE public.panoramas_adjacencies_new OWNER TO panorama;

--
-- Name: panoramas_mission; Type: TABLE; Schema: public; Owner: panorama
--

CREATE TABLE IF NOT EXISTS public.panoramas_mission (
    id integer NOT NULL,
    name text NOT NULL,
    date date,
    neighbourhood text,
    mission_type text NOT NULL,
    mission_year integer,
    surface_type character varying(1) NOT NULL,
    mission_distance integer NOT NULL
);


-- ALTER TABLE public.panoramas_mission OWNER TO panorama;

--
-- Name: panoramas_mission_id_seq; Type: SEQUENCE; Schema: public; Owner: panorama
--

CREATE SEQUENCE IF NOT EXISTS public.panoramas_mission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER TABLE public.panoramas_mission_id_seq OWNER TO panorama;

--
-- Name: panoramas_mission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: panorama
--

ALTER SEQUENCE public.panoramas_mission_id_seq OWNED BY public.panoramas_mission.id;


--
-- Name: panoramas_panorama_id_seq; Type: SEQUENCE; Schema: public; Owner: panorama
--

CREATE SEQUENCE IF NOT EXISTS public.panoramas_panorama_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER TABLE public.panoramas_panorama_id_seq OWNER TO panorama;

--
-- Name: panoramas_panorama_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: panorama
--

ALTER SEQUENCE public.panoramas_panorama_id_seq OWNED BY public.panoramas_panorama.id;


--
-- Name: panoramas_region; Type: TABLE; Schema: public; Owner: panorama
--

CREATE TABLE IF NOT EXISTS public.panoramas_region (
    id integer NOT NULL,
    region_type character varying(1) NOT NULL,
    left_top_x integer NOT NULL,
    left_top_y integer NOT NULL,
    right_top_x integer NOT NULL,
    right_top_y integer NOT NULL,
    left_bottom_x integer NOT NULL,
    left_bottom_y integer NOT NULL,
    right_bottom_x integer NOT NULL,
    right_bottom_y integer NOT NULL,
    detected_by character varying(255) NOT NULL,
    pano_id character varying(37) NOT NULL
);


-- ALTER TABLE public.panoramas_region OWNER TO panorama;

--
-- Name: panoramas_region_id_seq; Type: SEQUENCE; Schema: public; Owner: panorama
--

CREATE SEQUENCE IF NOT EXISTS public.panoramas_region_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER TABLE public.panoramas_region_id_seq OWNER TO panorama;

--
-- Name: panoramas_region_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: panorama
--

ALTER SEQUENCE public.panoramas_region_id_seq OWNED BY public.panoramas_region.id;


--
-- Name: panoramas_traject; Type: TABLE; Schema: public; Owner: panorama
--

CREATE TABLE IF NOT EXISTS public.panoramas_traject (
    id integer NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    geolocation extensions.geometry(PointZ,4326) NOT NULL,
    north_rms numeric(20,14) NOT NULL,
    east_rms numeric(20,14),
    down_rms numeric(20,14),
    roll_rms double precision,
    pitch_rms double precision,
    heading_rms double precision
);


-- ALTER TABLE public.panoramas_traject OWNER TO panorama;

--
-- Name: panoramas_traject_id_seq; Type: SEQUENCE; Schema: public; Owner: panorama
--

CREATE SEQUENCE IF NOT EXISTS public.panoramas_traject_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER TABLE public.panoramas_traject_id_seq OWNER TO panorama;

--
-- Name: panoramas_traject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: panorama
--

ALTER SEQUENCE public.panoramas_traject_id_seq OWNED BY public.panoramas_traject.id;


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: panorama
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: panorama
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: panoramas_mission id; Type: DEFAULT; Schema: public; Owner: panorama
--

ALTER TABLE ONLY public.panoramas_mission ALTER COLUMN id SET DEFAULT nextval('public.panoramas_mission_id_seq'::regclass);


--
-- Name: panoramas_panorama id; Type: DEFAULT; Schema: public; Owner: panorama
--

ALTER TABLE ONLY public.panoramas_panorama ALTER COLUMN id SET DEFAULT nextval('public.panoramas_panorama_id_seq'::regclass);


--
-- Name: panoramas_region id; Type: DEFAULT; Schema: public; Owner: panorama
--

ALTER TABLE ONLY public.panoramas_region ALTER COLUMN id SET DEFAULT nextval('public.panoramas_region_id_seq'::regclass);


--
-- Name: panoramas_traject id; Type: DEFAULT; Schema: public; Owner: panorama
--

ALTER TABLE ONLY public.panoramas_traject ALTER COLUMN id SET DEFAULT nextval('public.panoramas_traject_id_seq'::regclass);


