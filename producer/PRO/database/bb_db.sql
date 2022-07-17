--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: bucket_enum; Type: TYPE; Schema: public; Owner: postgres
--

SET default_tablespace = '';

SET default_with_oids = false;


CREATE TABLE IF NOT EXISTS building_block (
    id character varying(80) NOT NULL PRIMARY KEY,
    name_b character varying(128),
    address_b character varying(21),
    port integer NOT NULL,
    dockerfile character varying(128),
    volume_in_path text,
    volume_out_path text);

CREATE TABLE IF NOT EXISTS orders (
    id character varying(80) NOT NULL PRIMARY KEY,
    content_name text,
    status_o character varying(40),
    transaction_id character varying(80) NOT NULL,
    content_id text NOT NULL,
    iden text,
    logistic character varying(4),
    creation_date date DEFAULT now());

CREATE TABLE IF NOT EXISTS intra_orders (
    id character varying(80) NOT NULL PRIMARY KEY,
    id_orders character varying(80) NOT NULL,
    stage_id character varying(80) NOT NULL,
    status_o character varying(40),
    content_id text NOT NULL,
    logistic character varying(4),
    iden text,
    creation_date date DEFAULT now());

CREATE TABLE IF NOT EXISTS value_chain (
    id character varying(80) NOT NULL PRIMARY KEY,
    contract_id character varying(80) NOT NULL,
    valid_contract boolean,
    transaction_id character varying(80) NOT NULL,
    volume_in_path text,
    volume_out_path text,
    creation_date date DEFAULT now());

CREATE TABLE IF NOT EXISTS stage (
    id character varying(80) NOT NULL PRIMARY KEY,
    name_s character varying(120),
    executable_sentence character varying(120));

CREATE TABLE IF NOT EXISTS vc_stage (
    value_chain_id character varying(80) NOT NULL,
    stage_id character varying(80) NOT NULL,
    folder_in text NOT NULL,
    folder_out text NOT NULL,
    FOREIGN KEY (value_chain_id) REFERENCES value_chain (id),
    FOREIGN KEY (stage_id) REFERENCES stage (id),
    primary key(value_chain_id, stage_id));

ALTER TABLE orders OWNER TO postgres;
ALTER TABLE value_chain OWNER TO postgres;
ALTER TABLE stage OWNER TO postgres;
ALTER TABLE vc_stage OWNER TO postgres;