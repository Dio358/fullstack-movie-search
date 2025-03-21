"""
A file containing methods that call The Movie Database API
"""

import os
from typing import List, Any, Dict, Tuple

import requests
from flask import jsonify, Response
from flask.cli import load_dotenv

from ds_webapp.consume_api.utils import (
    create_movie_list,
    clean_data,
    create_ranked_movie_list,
    take_genre_set_difference,
)
from ds_webapp.consume_api.schemas import Movie

load_dotenv()
# setting API url and key
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


def get_movies_list(n: int) -> list[Any] | tuple[dict[str, str], int]:
    """
    Request a list of the n most popular movies,
    :param n: an int
    :precondition: 1 <= n <= 20
    :return:
    """

    headers = {"accept": "application/json", "Authorization": API_KEY}

    params = {"language": "en-US", "page": n}

    response = requests.get(
        f"{API_URL}/movie/popular", headers=headers, params=params, timeout=5
    )

    results = clean_data(response.json()["results"])

    if response.status_code == 200:
        return create_ranked_movie_list(
            movie_list=[Movie.model_validate(movie) for movie in results],
            length=n,
        )

    return (
        {"error": str(response.status_code), "message": response.text},
        response.status_code,
    )


def search_movie(title: str) -> list[Any] | tuple[dict[str, str], int]:
    """
    Search for movie in MovieDB
    :param title: movie title
    :return:
    """

    headers = {"accept": "application/json", "Authorization": API_KEY}

    params = {"language": "en-US", "query": title}

    response = requests.get(
        f"{API_URL}/search/movie", headers=headers, params=params, timeout=5
    )

    results = clean_data(response.json()["results"])

    if response.status_code == 200:
        return create_movie_list(
            movie_list=[Movie.model_validate(movie) for movie in results]
        )

    return {
        "error": str(response.status_code),
        "message": response.text,
    }, response.status_code


def search_movies_with_genres(
    genres_to_include: str, genres_to_exclude: str
) -> list[Any] | tuple[dict[str, str], int]:
    """
    Search for movie in MovieDB
    :param genres_to_exclude: list of genre ids to exclude
    :param genres_to_include: list of genre ids to include
    :return:
    """

    headers = {"accept": "application/json", "Authorization": API_KEY}

    params = {
        "language": "en-US",
        "with_genres": genres_to_include,
        "without_genres": genres_to_exclude,
    }

    response = requests.get(
        f"{API_URL}/discover/movie", headers=headers, params=params, timeout=5
    )

    results = clean_data(response.json()["results"])

    if response.status_code == 200:
        return create_movie_list(
            movie_list=[Movie.model_validate(movie) for movie in results],
        )

    return (
        {"error": str(response.status_code), "message": response.text},
        response.status_code,
    )


def get_movie_genres() -> list[Any] | tuple[dict[str, str], int]:
    """
     Get all movie genres from MovieDB
    :return:
    """

    headers = {"accept": "application/json", "Authorization": API_KEY}

    params = {"language": "en-US"}

    response = requests.get(
        f"{API_URL}/genre/movie/list", headers=headers, params=params, timeout=5
    )

    results = response.json()["genres"]

    if response.status_code == 200:
        return results

    return (
        {"error": str(response.status_code), "message": response.text},
        response.status_code,
    )


if __name__ == "__main__":
    # workflow of getting only movies with same genre as "Harry Potter and the Philosopher's Stone"
    genres = get_movie_genres()
    print(genres)
    genres_to_include = search_movie("Harry Potter and the Philosopher's Stone")[0][
        "genre_ids"
    ]
    genres_to_exclude = take_genre_set_difference(genres, genres_to_include)
    print(genres_to_exclude)
    print(genres_to_include)
    print(
        search_movies_with_genres(
            ",".join(str(id) for id in genres_to_include),
            ",".join(str(id) for id in genres_to_exclude),
        )
    )
