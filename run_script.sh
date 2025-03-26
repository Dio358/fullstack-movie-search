

# run tests
docker-compose run --rm app pytest

# run tests and show print statement output
docker-compose run --rm app pytest -s

# start up containers
# docker-compose up -d

# shut down containers
# docker-compose down -v

# shut down containters and empty db
# docker-compose down -v

