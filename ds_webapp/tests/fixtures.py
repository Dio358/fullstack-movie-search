import json
from pathlib import Path

import pytest

from ds_webapp.app import app
from ds_webapp.schemas import Movie


@pytest.fixture
def client():
    """Fixture to provide a Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture()
def movie_list_example():
    """Load test JSON data from file."""
    json_path = Path(__file__).parent / "test_movie_list.json"

    with open(json_path, "r", encoding="utf-8") as file:
        return [Movie.model_validate(movie) for movie in json.load(file)["results"]]
