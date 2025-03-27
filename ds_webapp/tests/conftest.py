"""
A file containing text fixtures
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

import pytest
import pytest_asyncio

from ds_webapp.app import app
from ds_webapp.consume_api.schemas import Movie
from ds_webapp.database.connect import Database

load_dotenv()


@pytest.fixture
def client():
    """
    Fixture to provide a Flask test client.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture()
def movie_list_example() -> list[Movie]:
    """
    Load test JSON data from file.
    """
    json_path = Path(__file__).parent / "test_movie_list.json"

    with open(json_path, "r", encoding="utf-8") as file:
        return [Movie.model_validate(movie) for movie in json.load(file)["results"]]


@pytest.fixture
def api_url() -> str:
    """
    Load API url from .env file
    """
    yield os.getenv("API_URL")


@pytest.fixture
def api_key() -> str:
    """
    Load API Key from .env file
    """
    yield os.getenv("API_KEY")


@pytest_asyncio.fixture
async def db():
    """
    returns database instance
    """
    db = Database()
    yield db
    await db.close()
