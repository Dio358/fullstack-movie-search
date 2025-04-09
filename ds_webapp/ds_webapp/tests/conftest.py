"""
A file containing text fixtures
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

import pytest
import pytest_asyncio
from flask import Flask, jsonify


from ds_webapp.app import app
from ds_webapp.consume_api.schemas import Movie
from ds_webapp.database.connect import Database
from ds_webapp.authentication.authentication import jwt_required

load_dotenv()


@pytest.fixture
def test_app():
    """
    Fixture to provide a Flask test app with a protected route
    """
    testapp = Flask(__name__)

    @testapp.route("/protected")
    @jwt_required
    def protected():
        return jsonify({"message": "Access granted"}), 200

    return testapp


@pytest.fixture
def client():
    """
    Fixture to provide a Flask test client.
    """
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture()
def movie_list_example() -> list[Movie]:
    """
    Load test JSON data from file.
    """
    json_path = Path(__file__).parent / "test_movie_list.json"

    with open(json_path, "r", encoding="utf-8") as file:
        return [Movie.model_validate(movie) for movie in json.load(file)["results"]]


@pytest.fixture
def api_url() -> str:  # type: ignore
    """
    Load API url from .env file
    """
    yield os.getenv("API_URL")


@pytest.fixture
def api_key() -> str:  # type: ignore
    """
    Load API Key from .env file
    """
    yield os.getenv("API_KEY")


@pytest_asyncio.fixture
async def db():
    """
    returns database instance
    """
    database = Database()
    yield database
    await database.close()
