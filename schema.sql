CREATE TABLE authors (
    id SERIAL PRIMARY KEY, 
    first_name TEXT, 
    surname TEXT, 
    born INTEGER,
    dead INTEGER,
    description TEXT);

CREATE TABLE material (
    id SERIAL PRIMARY KEY,
    name TEXT,
    author_id INTEGER,
    issued INTEGER,
    amount INTEGER,
    type_id INTEGER,
    age INTEGER);

CREATE TABLE types (
    id SERIAL PRIMARY KEY,
    name TEXT);

INSERT INTO types (name) VALUES ('Kirja');
INSERT INTO types (name) VALUES ('Lehti');
INSERT INTO types (name) VALUES ('Blue-ray-levy');
INSERT INTO types (name) VALUES ('Muu');
INSERT INTO types (name) VALUES ('DVD-levy');
INSERT INTO types (name) VALUES ('CD-levy');

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name TEXT,
    username TEXT,
    password TEXT,
    age INTEGER);
