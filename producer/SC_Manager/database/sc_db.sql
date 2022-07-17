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
    description_text text);


CREATE TABLE IF NOT EXISTS company (
    id character varying(80) NOT NULL PRIMARY KEY,
    name_c character varying(128),
    email character varying(128),
    password_c character varying(260),
    address_c character varying(21) NOT NULL,
    port integer NOT NULL);

CREATE TABLE IF NOT EXISTS contract_sc (
    id character varying(80) NOT NULL PRIMARY KEY,
    type_sc character varying(6),
    name_sc character varying(128),
    address_sc character varying(21) NOT NULL,
    port integer NOT NULL,
    valid_contract boolean,
    transaction_id character varying(80) NOT NULL,
    volume_in_path text,
    volume_out_path text,
    building_block_id character varying(80) NOT NULL);

CREATE TABLE IF NOT EXISTS orders (
    id character varying(80) NOT NULL PRIMARY KEY,
    content_name text,
    iden text,
    previous_order_id character varying (80),
    creation_date date DEFAULT now(),
    status_o character varying(80),
    transaction_id character varying(80) NOT NULL,
    content_id text NOT NULL,
    logistic character varying(4));

CREATE TABLE IF NOT EXISTS supply_chain (
    id character varying(80) NOT NULL PRIMARY KEY,
    creation_date date DEFAULT now(),
    contract_id character varying(80) NOT NULL,
    catalog_in text,
    catalog_out text);

ALTER TABLE building_block OWNER TO postgres;
ALTER TABLE company OWNER TO postgres;
ALTER TABLE contract_sc OWNER TO postgres;
ALTER TABLE orders OWNER TO postgres;
ALTER TABLE supply_chain OWNER TO postgres;