"""
A file containing methods that call The Movie Database API
"""

import os
from typing import Any

import requests
from flask.cli import load_dotenv

from ds_webapp.consume_api.schemas import Movie

load_dotenv()

# setting API url and key
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


def get_popular_movies() -> list[Any] | tuple[dict[str, str], int]:
    """
    Request a list of the n most popular movies,
    :param n: an int
    :precondition: 1 <= n <= 20
    :return:
    """

    headers = {"accept": "application/json", "Authorization": API_KEY}

    params = {"language": "en-US"}

    response = requests.get(
        f"{API_URL}/movie/popular", headers=headers, params=params, timeout=5
    )

    if response.status_code == 200:
        return response.json().get("results")

    raise response


def search_movie(title: str) -> list[Movie] | tuple[dict[str, str | int], int]:
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

    if response.status_code == 200:
        return response.json().get("results")

    raise response


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

    if response.status_code == 200:
        return response.json().get("results")

    raise response


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

    if response.status_code == 200:
        return response.json().get("genres")

    raise response


def get_movie_details(movie_id: int) -> list[dict[str, int | str | None]]:
    """
    Get detail info about movie from movie_db
    :param movie_id: unique id of movie
    """

    headers = {"accept": "application/json", "Authorization": API_KEY}

    params = {"language": "en-US"}

    response = requests.get(
        f"{API_URL}/movie/{movie_id}", headers=headers, params=params, timeout=5
    )

    if response.status_code == 200:

        return response.json()

    raise response


def search_movies_with_duration(min_duration: int, max_duration: int) -> list[Movie]:
    """
     Get movies from MovieDB with a duration: min_duration <= duration <= max_duration
     :param min_duration: minimum duration
     :param max_duration: maximum duration
    :return:
    """

    headers = {"accept": "application/json", "Authorization": API_KEY}

    params = {
        "language": "en-US",
        "with_runtime.gte": min_duration,
        "with_runtime.lte": max_duration,
    }

    response = requests.get(
        f"{API_URL}/discover/movie", headers=headers, params=params, timeout=5
    )

    if response.status_code == 200:

        return response.json().get("results")

    raise response


if __name__ == "__main__":
    # # workflow of getting only movies with same genre as "Harry Potter and the Philosopher's Stone"
    # genres = get_movie_genres()
    # print(genres)
    # genres_to_include = search_movie("Harry Potter and the Philosopher's Stone")[0][
    #     "genre_ids"
    # ]
    # genres_to_exclude = take_genre_set_difference(genres, genres_to_include)
    # print(genres_to_exclude)
    # print(genres_to_include)
    # print(
    #     search_movies_with_genres(
    #         ",".join(str(id) for id in genres_to_include),
    #         ",".join(str(id) for id in genres_to_exclude),
    #     )
    # )

    # workflow for getting movies with duration +- 10 of duration of certain movie
    result2 = get_movie_details(970450)
    print(result2)

    result = search_movies_with_duration(90, 100)
    print(result)
