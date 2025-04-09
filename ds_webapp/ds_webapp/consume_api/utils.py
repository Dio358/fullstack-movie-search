"""
A file with utils to create and parse responses
"""

from typing import Union, List, Dict
from ds_webapp.consume_api.schemas import Movie


def clean_data(
    results: list[dict[str, int | str]],
) -> list[dict[str, int | str | None]]:
    """
    Clean movie data, replace "" release date with None
    :param results: JSON of movie results
    :return: Cleaned list of movie dicts
    """
    for result in results:
        if result.get("release_date") == "":
            result["release_date"] = None
    return results


def create_ranked_movie_list(
    movie_list: list[Movie], length: int
) -> list[dict[str : int | str]]:
    """
    A function which takes creates a list of the 'length' most popular movies
    :param ranked: boolean to increase a rank
    :param movie_list: list of movies
    :param length: desired length of the list
    :return:
    """
    return [{"rank": i + 1, "title": movie_list[i].title} for i in range(length)]


def create_movie_list(movie_list: list[Movie]) -> list[dict[str : int | str]]:
    """
    A function which takes creates a list of the 'length' most popular movies
    :param movie_list: list of movies
    :return:
    """
    return [
        {"title": movie.title, "genre_ids": movie.genre_ids} for movie in movie_list
    ]


def take_genre_set_difference(
    genre_list: List[Dict[str, Union[str, int]]], to_exclude: List[int]
) -> list[int]:
    """
    Takes list of all possible genres and excludes genres listed in to_exlude
    :param genre_list: list of all possible genres
    :param to_exclude: genres to exclude from list
    :return:
    """
    result = []
    for genre in genre_list:
        if genre["id"] not in to_exclude:
            result.append(genre["id"])
    return result
