-- ============================================================
-- EasyX / db / bootstrap.sql
-- Purpose:
--   1) ensure role "easyxapp" (with password)
--   2) ensure database "easyxdb" (owned by easyxapp)
--   3) Connect to easyxdb, transfer "public" schema ownership/privileges
--   4) Run init_tables.sql as easyxapp so new objects are owned by it
--
-- How to run (must use psql because of \connect, \if, \gset, \gexec, \ir):
--   psql -v ON_ERROR_STOP=1 -v VERBOSITY=verbose -v ECHO=all --echo-errors -a \
--        -d postgres -f /EasyX/db/bootstrap.sql
--
-- Terminal output:
--   - \echo step banners (human-friendly)
--   - ECHO all + \timing on => every statement echoed with timing
--   - Errors are verbose due to VERBOSITY=verbose
-- ============================================================

-- Session options (do NOT put inline comments on backslash lines)
\set ON_ERROR_STOP 1
\set VERBOSITY verbose
\set ECHO all
\timing on
\pset pager off

-- Configurable variables (psql variables)
\set dbname 'easyxdb'
\set appuser 'easyxapp'
\set apppass 'easyxpass'

\echo ========================================================================
\echo === EasyX DB Bootstrap: role/db/schema ownership + init_tables.sql   ===
\echo ========================================================================

-- [1/6] Ensure role :appuser (LOGIN, password)
\echo -- [1/6] Ensure role :appuser (LOGIN, password) ...

-- Compute role existence into a psql variable "role_exists"
-- NOTE: do not end this SELECT with a semicolon when using \gset
SELECT (EXISTS(SELECT 1 FROM pg_roles WHERE rolname = :'appuser'))::int AS role_exists \gset

\if :role_exists
  \echo NOTICE: Role :appuser exists; ensuring LOGIN/password...
  -- Ensure LOGIN + password
  SELECT format('ALTER ROLE %I LOGIN PASSWORD %L', :'appuser', :'apppass') \gexec
\else
  \echo NOTICE: Creating role :appuser ...
  -- Create role with LOGIN + password
  SELECT format('CREATE ROLE %I LOGIN PASSWORD %L', :'appuser', :'apppass') \gexec
\endif

-- [2/6] Ensure database :dbname (owned by :appuser)
\echo -- [2/6] Ensure database :dbname (owned by :appuser) ...

-- Always return exactly one row: 1 if exists, 0 otherwise
SELECT (EXISTS(SELECT 1 FROM pg_database WHERE datname = :'dbname'))::int AS db_exists \gset

\if :db_exists
  \echo NOTICE: Database :dbname already exists; ensuring owner :appuser ...
  -- Keep ownership consistent (safe even if already correct)
  ALTER DATABASE :dbname OWNER TO :appuser;
\else
  \echo NOTICE: Creating database :dbname owned by :appuser ...
  CREATE DATABASE :dbname OWNER :appuser;
\endif

-- [3/6] Connect to the target database
\echo -- [3/6] Connect to :dbname ...
\connect :dbname

-- [4/6] Transfer schema ownership and grant privileges
\echo -- [4/6] Transfer public schema ownership and grant privileges ...
ALTER SCHEMA public OWNER TO :appuser;
GRANT USAGE, CREATE ON SCHEMA public TO :appuser;

-- Optional: make privileges future-proof for new objects created by :appuser
-- (Does not change owner; owner is determined by SET ROLE below)
ALTER DEFAULT PRIVILEGES FOR ROLE :appuser IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO :appuser;
ALTER DEFAULT PRIVILEGES FOR ROLE :appuser IN SCHEMA public
GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO :appuser;

-- [5/6] Use role :appuser so new objects will be owned by it
\echo -- [5/6] Use role :appuser so new objects are owned by it ...
SET ROLE :appuser;
SELECT current_user AS current_user, session_user AS session_user;

-- [6/6] Include and execute init_tables.sql as :appuser
\echo -- [6/6] Run init_tables.sql (tables + seed data) as :appuser ...
\ir init_tables.sql

\echo ========================================================================
\echo === Bootstrap finished. All new objects are owned by role: :appuser  ===
\echo ========================================================================
