# Full-Stack Movie App

This project demonstrates the design and deployment of a production-style fullstack application, with a focus on backend architecture, API design, and containerized systems.

## Key Features

- Fullstack architecture (Flask + React + PostgreSQL)
- JWT-based authentication
- Dockerized deployment (production-style setup)
- RESTful API design
- Movie recommendation logic based on similarity

## Engineering Highlights

- Designed a full 3-tier architecture (frontend, backend, database)
- Implemented stateless authentication using JWT
- Built and containerized the entire system using Docker Compose
- Developed custom recommendation logic based on genre and runtime similarity
  
## Project Structure

- **Backend**: Flask REST API (`ds_webapp`)
- **Frontend**: React + TypeScript (`ui-vite`)
- **Database**: PostgreSQL with user & favorite movie tables
- **Containerization**: Full Docker Compose setup
- **Authentication**: JWT-based, stateless
 
## Prerequisites

- [Docker](https://www.docker.com/) installed
- [Node.js](https://nodejs.org/) (if running the frontend separately in dev mode)


## Running the App

### 1. Get a Bearer Token

Create a free account on [The Movie Database (TMDB)](https://www.themoviedb.org/) and generate an API Read Access Token (v4 auth) from your [API settings](https://www.themoviedb.org/settings/api).  
This token is required to fetch movie data from their API.


### 2. Create `.env` file

In the [`./ds_webapp/ds_webapp`](./ds_webapp/ds_webapp) directory, create a file named `.env` and add the following contents:

```env
# External API config
API_URL="https://api.themoviedb.org/3/"
API_KEY="Bearer <your-Bearer-Token>"  # Replace with your actual TMDB token

# PostgreSQL config
POSTGRES_USER=pgres
POSTGRES_PASSWORD=pgres
POSTGRES_DB=pgres
POSTGRES_HOST=host.docker.internal
POSTGRES_PORT=5432

# App secret for JWT signing
SECRET_KEY=student.uantwerpen.be
```

 Don't forget to replace `<your-Bearer-Token>` with the token from TMDB.


### 3. Start the App

Run this script to build and start all services using Docker Compose:

```bash
./run_api.sh
```

Or start manually:

```bash
docker compose up --build
```


### 4. Access the App

Once running, the app will be available at:

- **Frontend**: [http://localhost:3000](http://localhost:3000)  
  React app with login, search, and favorites tabs

- **Backend API**: [http://localhost:5000](http://localhost:5000)  
  Flask RESTful API powering the frontend and handling user auth, favorites, and movie fetching

## Running Tests

To run backend tests inside the container:

```bash
docker compose exec app poetry run pytest
```

## API Design

- RESTful API built with Flask
- Stateless authentication using JWT
- Structured endpoints with proper HTTP status codes
- Separation between business logic, routing, and data access


## Fault Tolerance

Each endpoint includes specific error handling with proper status codes:
- 201 for successful creations
- 409 if username already exists
- 500 for general server errors

Example from the user creation route:

```python
except asyncpg.UniqueViolationError:
    return jsonify({"error": "Username already exists"}), 409
```


## Features & Extensions

### Authentication
- JWT token generation on login (3h validity)
- Credentials securely stored using hashing
- Implemented in [authentication.py](ds_webapp/ds_webapp/authentication/authentication.py)

### Frontend
Built in Vite + React + TypeScript  
Located in [`ui-vite/`](./ui-vite)

Includes:
- **Popular Tab**: Browse trending movies
- **Favorites Tab**: View and compare favorited movies with charts
- **Search Tab**: Discover similar movies by genre and runtime

Caching and UI state are handled via Redux:  
[`ui-vite/src/redux`](./ui-vite/src/redux)

### Recommendation Logic
- Custom logic to find movies with similar genre and runtime (+/- 10 min)
- Data pulled and filtered from the TMDB API

### Database
PostgreSQL schema includes:
```sql
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
```

Schema is initialized via:
- [`init-db/init-db.sql`](./init-db/init-db.sql)

### Dockerized Setup

Docker Compose orchestrates the full stack:

- `db`: PostgreSQL container, pre-seeded
- `app`: Flask backend
- `frontend`: React + Vite client

Config in [docker-compose.yml](./docker-compose.yml)

## Scripts

- [`run_api.sh`](./run_api.sh): Starts the backend and DB containers
- [`run_script.sh`](./run_script.sh): Example script runner
- [`consume_api.py`](./ds_webapp/ds_webapp/tests/test_consume_api.py): Sample test client

## Performance & Scalability

- Basic caching implemented on client and server side
- Docker-based setup allows for scalable deployment
- Architecture designed with separation of concerns for future extensibility


## Design Decisions

- Chose PostgreSQL for realistic scalability, though SQLite would’ve worked for demo purposes
- Opted for a 3-tier architecture to practice separation of concerns and modularity
- Kept logic close to real-world deployments to use this as a showcase project


## Author

**Dio Ngei Okparaji**  
[LinkedIn](www.linkedin.com/in/dio-ngei-okparaji-3769b4171) · [GitHub](https://github.com/Dio358)
