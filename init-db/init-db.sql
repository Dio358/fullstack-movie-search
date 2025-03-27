CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS favorites (
    movie_id INT,
    user_id INT REFERENCES users(id),
    PRIMARY KEY(movie_id, user_id)
);