CREATE TABLE authors (
    id SERIAL PRIMARY KEY, 
    first_name TEXT, 
    surname TEXT, 
    born INTEGER,
    dead INTEGER,
    description TEXT);

CREATE TABLE librarymaterial (
    id SERIAL PRIMARY KEY,
    name TEXT,
    author_id INTEGER,
    issued INTEGER,
    amount INTEGER,
    type_id INTEGER,
    age INTEGER);

CREATE TABLE materialtypes (
    id SERIAL PRIMARY KEY,
    name TEXT);

INSERT INTO materialtypes (name) VALUES ('Kirja');
INSERT INTO materialtypes (name) VALUES ('Lehti');
INSERT INTO materialtypes (name) VALUES ('Blue-ray-levy');
INSERT INTO materialtypes (name) VALUES ('Muu');
INSERT INTO materialtypes (name) VALUES ('DVD-levy');
INSERT INTO materialtypes (name) VALUES ('CD-levy');

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name TEXT,
    username TEXT UNIQUE,
    password TEXT,
    age INTEGER);
