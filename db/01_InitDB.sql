-- Initialize the DB with the default admin user
-- with the correct privileges
DROP ROLE IF EXISTS qa;

CREATE ROLE qa WITH LOGIN PASSWORD 'qatest';
ALTER ROLE qa CREATEDB;

CREATE DATABASE qadashboard;
GRANT ALL PRIVILEGES ON DATABASE qadashboard TO qa;

