CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT
);

CREATE TABLE IF NOT EXISTS favorites (
    movie_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
);