


CREATE TABLE authors (
    id SERIAL PRIMARY KEY, 
    first_name TEXT, 
    surname TEXT NOT NULL, 
    description TEXT
);

CREATE TABLE librarymaterial (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    author_id INTEGER REFERENCES authors,
    issued INTEGER,
    amount INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    age INTEGER
);

CREATE TABLE materialtypes (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

INSERT INTO materialtypes (name) VALUES ('Kirja');
INSERT INTO materialtypes (name) VALUES ('Lehti');
INSERT INTO materialtypes (name) VALUES ('Blue-ray-levy');
INSERT INTO materialtypes (name) VALUES ('Muu');
INSERT INTO materialtypes (name) VALUES ('DVD-levy');
INSERT INTO materialtypes (name) VALUES ('CD-levy');

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    age INTEGER,
    access TEXT NOT NULL DEFAULT 'user'
);

CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts ON DELETE CASCADE,
    material_id INTEGER REFERENCES librarymaterial,
    returned BOOLEAN NOT NULL DEFAULT False
);

--UPDATE accounts SET username='paakayttaja', access='admin' WHERE id=1;

