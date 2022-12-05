-- Create User Database
CREATE USER uoncourse WITH ENCRYPTED PASSWORD 'PwDoncourseSatu1Dua3';

-- Create Database
CREATE DATABASE db_oncourse;

GRANT ALL ON ALL TABLES IN SCHEMA public to uoncourse;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to uoncourse;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to uoncourse;