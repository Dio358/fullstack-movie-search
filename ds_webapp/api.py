"""
A file containing the app's API.
"""

from http.client import HTTPException
from typing import Tuple, List, Any, Dict

from flasgger import swag_from
from flask import Response
from flask_restful import Resource, Api

from ds_webapp.consume_api.consume_api import (
    get_popular_movies,
    get_movie_genres,
    search_movie,
    search_movies_with_genres,
)
from ds_webapp.consume_api.utils import take_genre_set_difference


class Welcome(Resource):
    """
    A class welcoming the user to the webpage.
    """

    @swag_from(
        {
            "tags": ["Welcome"],
            "responses": {
                200: {
                    "description": "A status code 200 means successful and returns a message.",
                    "content": {
                        "application/json": {
                            "message": "Welcome to the movie list app!! Please go to apidocs to see the endpoint swagger!"
                        }
                    },
                }
            },
        }
    )
    def get(self) -> Response:
        """
        Returns a welcome message.

        :return: 200 OK with a welcome message.
        """
        return Response(
            {
                "Welcome to the movie list app!! Please go to apidocs to see the endpoint swagger!"
            },
            200,
        )


class Movies(Resource):
    """
    A class to send requests related to movies.
    """

    @swag_from(
        {
            "tags": ["Movies"],
            "responses": {
                200: {
                    "description": "Returns a welcome message from the Movies endpoint.",
                    "content": {
                        "application/json": {
                            "message": "Welcome to the movie list app!! Please go to apidocs to see the endpoint swagger!"
                        }
                    },
                }
            },
        }
    )
    def get(self) -> Response:
        """
        Returns a welcome message from the Movies endpoint.

        :return: 200 OK with a welcome message.
        """
        return Response(
            {
                "Welcome to the movie list app!! Please go to apidocs to see the endpoint swagger!"
            },
            200,
        )


class MostPopular(Movies):
    """
    A class to send requests related to the most popular movies.
    """

    @swag_from(
        {
            "tags": ["Movies"],
            "parameters": [
                {
                    "name": "n",
                    "in": "path",
                    "type": "integer",
                    "required": False,
                    "description": "The number of movies to retrieve (1-20).",
                }
            ],
            "responses": {
                200: {
                    "description": "Returns a list of the n most popular movies.",
                    "content": {
                        "application/json": {
                            "examples": {
                                "example1": {
                                    "summary": "Successful response",
                                    "value": [
                                        {"title": "Movie 1"},
                                        {"title": "Movie 2"},
                                    ],
                                }
                            }
                        }
                    },
                },
                400: {
                    "description": "Invalid value for 'n'. Must be between 1 and 20.",
                },
                500: {
                    "description": "Internal server error.",
                },
            },
        }
    )
    def get(self, n: int = 1) -> Tuple[List[Any], int] | Tuple[Dict[str, str], int]:
        """
        Returns a list of the n most popular movies.

        :param n: Number of movies to return (default = 1). Must be between 1 and 20.
        :return:
            - 200 OK with list of movies
            - 400 Bad Request if n is out of range
            - 500 Internal Server Error for unhandled exceptions
        """
        try:
            if not 1 <= n <= 20:
                return {
                    "error": "Invalid value for 'n'. It should be between 1 and 20."
                }, 400

            return get_popular_movies()[:n], 200
        except HTTPException as e:
            return e
        except Exception as e:
            return {"error": "Internal server error"}, 500


class MoviesWithSameGenres(Movies):
    """
    A class to send requests related to movies with the same genres.
    """

    @swag_from(
        {
            "tags": ["Movies"],
            "parameters": [
                {
                    "name": "movie",
                    "in": "path",
                    "type": "string",
                    "required": True,
                    "description": "The title of the movie to find similar genre matches for.",
                }
            ],
            "responses": {
                200: {
                    "description": "Returns a list of movies with the same genres as the input movie.",
                    "content": {
                        "application/json": {
                            "examples": {
                                "example1": {
                                    "summary": "Successful response",
                                    "value": [
                                        {"title": "Movie 1"},
                                        {"title": "Movie 2"},
                                    ],
                                }
                            }
                        }
                    },
                },
                400: {
                    "description": "Invalid input value.",
                },
                404: {
                    "description": "Not found.",
                },
                500: {
                    "description": "Internal server error.",
                },
            },
        }
    )
    def get(
        self, movie: str
    ) -> Tuple[List[Any], int] | Tuple[Dict[str, str], int] | Tuple[str, int]:
        """
        Returns a list of movies that share all genres with the given movie.

        :param movie: Title of the movie to search by.
        :return:
            - 200 OK with list of matching movies
            - 404 Not Found if the movie does not exist
            - 500 Internal Server Error for unexpected failures
        """
        try:
            genres = get_movie_genres()
            search_result = search_movie(movie)

            if not search_result:
                return {"error": "Not Found."}, 404

            genres_to_include = search_result[0].get("genre_ids")
            assert genres is not None, "No genres found"

            genres_to_exclude = take_genre_set_difference(genres, genres_to_include)

            movies = search_movies_with_genres(
                ",".join(str(id) for id in genres_to_include),
                ",".join(str(id) for id in genres_to_exclude),
            )
            return movies, 200

        except HTTPException as e:
            return e
        except Exception as e:
            return {"error": "Internal server error"}, 500


def add_endpoints(api: Api) -> None:
    """
    Adds endpoints to the application's RESTful API.

    :param api: Flask-RESTful API object.
    """
    api.add_resource(Welcome, "/")
    api.add_resource(Movies, "/movies")
    api.add_resource(
        MostPopular, "/movies/most_popular", "/movies/most_popular/<int:n>"
    )
    api.add_resource(MoviesWithSameGenres, "/movies/same_genres/<string:movie>")


if __name__ == "__main__":
    movie = "Harry Potter"
    search_result = search_movie(movie)
    print(search_result)
    print(len(search_result))
    if len(search_result) == 0:
        print("No movie found")

    # genres = get_movie_genres()
    # search_result = search_movie("Harry Potter and the Philosopher's Stone")
    #
    # if not search_result:
    #     print("error: Not Found.", 404)
    #     exit(1)
    #
    # genres_to_include = search_result[0].get("genre_ids")
    # assert genres is not None, "No genres found"
    #
    # genres_to_exclude = take_genre_set_difference(genres, genres_to_include)
    #
    # movies = search_movies_with_genres(
    #     ",".join(str(id) for id in genres_to_include),
    #     ",".join(str(id) for id in genres_to_exclude),
    # )
    #
    # print(movies)
