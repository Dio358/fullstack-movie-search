"""
A file containing methods that call The Movie Database API
"""

import os

import requests
from flask import jsonify, Response

from ds_webapp.consume_api.movie_utils import create_movie_list
from ds_webapp.consume_api.schemas import Movie

# setting API url and key
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


def get_movies_list(n: int) -> Response | tuple[Response, int]:
    """
    Request a list of the n most popular movies,
    :param n: an int
    :precondition: 1 <= n <= 20
    :return:
    """

    # n = request.args.get("n", default=1, type=int)

    headers = {"accept": "application/json", "Authorization": API_KEY}

    params = {"language": "en-US", "page": n}

    response = requests.get(
        f"{API_URL}/movie/popular", headers=headers, params=params, timeout=5
    )

    if response.status_code == 200:
        return jsonify(
            create_movie_list(
                movie_list=[
                    Movie.model_validate(movie) for movie in response.json()["results"]
                ],
                length=n,
            )
        )

    return (
        jsonify({"error": str(response.status_code), "message": response.text}),
        response.status_code,
    )
