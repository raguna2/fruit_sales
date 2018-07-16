CREATE ROLE myprojectuser WITH LOGIN PASSWORD 'password';
CREATE DATABASE myproject;
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'ASIA/TOKYO';
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
\q
