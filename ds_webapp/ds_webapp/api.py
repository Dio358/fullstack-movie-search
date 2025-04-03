"""
A file containing the app's API.
"""

from http.client import HTTPException
from typing import Tuple, List, Any, Dict
import asyncio

import asyncpg
from flasgger import swag_from
from flask import Response, jsonify, request
from flask_restful import Resource, Api, reqparse


from ds_webapp.authentication.authentication import create_jwt_token, jwt_required
from ds_webapp.consume_api.consume_api import (
    get_popular_movies,
    get_movie_genres,
    search_movie,
    search_movies_with_genres,
    get_movie_details,
    search_movies_with_duration,
)
from ds_webapp.consume_api.utils import take_genre_set_difference
from ds_webapp.database.connect import Database
from ds_webapp.database.tables import Favorites, Users

db = Database()


class Welcome(Resource):
    """
    A class welcoming the user to the webpage.
    """

    @swag_from(
        {
            "tags": ["Welcome"],
            "security": [{"BearerAuth": []}],
            "responses": {
                200: {
                    "description": "A status code 200 means successful and returns a message.",
                    "content": {
                        "application/json": {
                            "example": {
                                "message": "Welcome to the movie list app!! Please go to apidocs to see the endpoint swagger!"
                            }
                        }
                    },
                }
            },
        }
    )
    def get(self):
        """
        Returns a welcome message.
        """
        return jsonify(
            {
                "message": "Welcome to the movie list app!! Please go to apidocs to see the endpoint swagger!"
            }
        )


class Movies(Resource):
    """
    A class to send requests related to movies.
    """

    @swag_from(
        {
            "tags": ["Movies"],
            "security": [{"BearerAuth": []}],
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
    @jwt_required
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


class MostPopular(Resource):
    """
    A class to send requests related to the most popular movies.
    """

    @swag_from(
        {
            "tags": ["Movies"],
            "security": [{"BearerAuth": []}],
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
    @jwt_required
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
        # pylint: disable=locally-disabled, broad-exception-caught
        except Exception as e:
            print("exception: ", e)
            return {"error": "Internal server error"}, 500


class MoviesWithSameGenres(Resource):
    """
    A class to send requests related to movies with the same genres.
    """

    @swag_from(
        {
            "tags": ["Movies"],
            "security": [{"BearerAuth": []}],
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
    @jwt_required
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
        # pylint: disable=locally-disabled, broad-exception-caught
        except Exception as e:
            print("exception: ", e)
            return {"error": "Internal server error"}, 500


class MoviesWithSimilarRuntime(Resource):
    """
    A class to send requests relates to movies with similar runtimes
    """

    @swag_from(
        {
            "tags": ["Movies"],
            "security": [{"BearerAuth": []}],
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
    @jwt_required
    def get(
        self, movie: str
    ) -> Tuple[List[Any], int] | Tuple[Dict[str, str], int] | Tuple[str, int]:
        """
        Given a movie, returns movies with a similar runtime (+- 10 minutes).

        :param movie: Title of the movie to search by.
        :return:
            - 200 OK with list of matching movies
            - 404 Not Found if the movie does not exist
            - 500 Internal Server Error for unexpected failures
        """
        try:
            search_result = search_movie(movie)

            if not search_result:
                return {"error": "Not Found."}, 404

            movie_id = search_result[0].get("id")
            assert movie_id is not None, "Unknown movie_id"

            detailed_search_result = get_movie_details(movie_id)

            if not detailed_search_result:
                return {"error": "Not Found."}, 404

            duration = detailed_search_result.get("runtime")
            assert duration is not None, "Movie duration not found"

            result = search_movies_with_duration(
                min_duration=duration - 10, max_duration=duration + 10
            )
            assert result is not None, "Movies with similar duration not found"

            return result, 200

        except HTTPException as e:
            return e
        # pylint: disable=locally-disabled, broad-exception-caught
        except Exception as e:
            print("error:", e)
            return {"error": "Internal server error"}, 500


class CreateUser(Resource):
    """
    A class that handles user creation
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            help="Username is required",
            location="json",
        )
        self.reqparse.add_argument(
            "password",
            type=str,
            required=True,
            help="Password is required",
            location="json",
        )
        super(CreateUser, self).__init__()

    @swag_from(
        {
            "tags": ["Users"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "password": {"type": "string"},
                        },
                        "required": ["username", "password"],
                    },
                }
            ],
            "responses": {
                200: {"description": "User created successfully"},
                400: {"description": "Invalid input"},
                409: {"description": "Username already exists"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def post(self):
        """
        A function to send a post request to create a new user
        """
        args = self.reqparse.parse_args()
        username = args["username"]
        password = args["password"]
        user_table = Users(db=db)

        async def create_user_async():
            return await user_table.add_user(username=username, password=password)

        try:
            result = async_request(create_user_async)

            if result:
                return {"message": f"User {username} created successfully"}, 200
            else:
                return {"error": "Username already exists"}, 409

        except asyncpg.UniqueViolationError:
            return {"error": "Username already exists"}, 409
        except Exception as e:
            print(f"Internal error: {e}")
            return {"error": f"User creation failed: {e}"}, 500


class Login(Resource):
    """
    A class that handles user creation
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            help="Username is required",
            location="json",
        )
        self.reqparse.add_argument(
            "password",
            type=str,
            required=True,
            help="Password is required",
            location="json",
        )
        super(Login, self).__init__()

    @swag_from(
        {
            "tags": ["Login"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "password": {"type": "string"},
                        },
                        "required": ["username", "password"],
                    },
                }
            ],
            "responses": {
                200: {"description": "login successfull"},
                400: {"description": "Invalid input"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def post(self):
        """
        A function to send a post request to log in
        """
        args = self.reqparse.parse_args()
        username = args["username"]
        password = args["password"]
        user_table = Users(db=db)

        async def login():
            return await user_table.get_user_id(username=username, password=password)

        try:
            uid = async_request(login)
            if uid:
                token = create_jwt_token(
                    {
                        "user_id": uid,
                        "username": "JohnDoe123",
                    }
                )
                return {"message": "login successful!", "token": f"{token}"}, 200

            return {"error": "Unathorized"}, 401
        except Exception as e:
            print(f"Internal error: {e}")
            return {"error": "Internal server error."}, 500


class FavoriteMovies(Resource):
    """
    Get the list of favorite movies for the authenticated user
    """

    @swag_from(
        {
            "tags": ["Favorites"],
            "security": [{"BearerAuth": []}],
            "summary": "Get user's favorite movies",
            "description": "Retrieve a list of movies marked as favorites by the authenticated user",
            "responses": {
                200: {
                    "description": "Successfully retrieved favorite movies",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "favorites": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "movie_id": {"type": "integer"},
                                        "title": {"type": "string"},
                                        "genre": {"type": "string"},
                                        "added_at": {
                                            "type": "string",
                                            "format": "date-time",
                                        },
                                    },
                                },
                            }
                        },
                    },
                },
                401: {"description": "Unauthorized - Invalid or missing JWT token"},
                500: {"description": "Internal server error"},
            },
        }
    )
    @jwt_required
    def get(self):
        user_id = request.user["user_id"]
        favorites_table = Favorites(db=db)

        async def get_favorites():
            return await favorites_table.get_favorites(user_id=user_id)

        try:
            result = async_request(get_favorites)

            if result:
                return {
                    "result": [
                        get_movie_details(dict(row).get("movie_id")) for row in result
                    ]
                }, 200
        except Exception as e:
            return {"message": f"Internal server error {e}"}, 500


class AddFavorite(Resource):
    @swag_from(
        {
            "tags": ["Favorites"],
            "security": [{"BearerAuth": []}],
            "summary": "Add a movie to favorites",
            "description": "Add a specific movie to the user's favorites list",
            "parameters": [
                {
                    "name": "movie_id",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                    "description": "Unique identifier of the movie to add",
                }
            ],
            "responses": {
                201: {"description": "Movie successfully added to favorites"},
                401: {"description": "Unauthorized - Invalid or missing JWT token"},
                409: {"description": "Movie already exists in favorites"},
                500: {"description": "Internal server error"},
            },
        }
    )
    @jwt_required
    def post(self, movie_id):
        user_id = request.user["user_id"]

        favorites_table = Favorites(db=db)

        async def like_movie():
            return await favorites_table.like_movie(user_id=user_id, movie_id=movie_id)

        try:
            async_request(like_movie)
            return {"message": "OK"}, 201
        except Exception as e:
            return {"message": f"Internal server error: {e}"}, 500


class RemoveFavorite(Resource):
    @swag_from(
        {
            "tags": ["Favorites"],
            "security": [{"BearerAuth": []}],
            "summary": "Remove a movie from favorites",
            "description": "Delete a specific movie from the user's favorites list",
            "parameters": [
                {
                    "name": "movie_id",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                    "description": "Unique identifier of the movie to remove",
                }
            ],
            "responses": {
                200: {"description": "Movie successfully removed from favorites"},
                401: {"description": "Unauthorized - Invalid or missing JWT token"},
                404: {"description": "Movie not found in favorites"},
                500: {"description": "Internal server error"},
            },
        }
    )
    @jwt_required
    def delete(self, movie_id):
        user_id = request.user["user_id"]
        favorites_table = Favorites(db=db)

        async def unlike_movie():
            return await favorites_table.unlike_movie(
                user_id=user_id, movie_id=movie_id
            )

        try:
            async_request(unlike_movie)
            return {
                "message": "OK",
                "movie_id": movie_id,
            }, 200
        except Exception:
            return {"message": "Internal server error"}, 500


class SearchMovie(Resource):
    """
    Search for movies by title using the MovieDB API
    """

    @swag_from(
        {
            "tags": ["Movies"],
            "security": [{"BearerAuth": []}],
            "summary": "Search movies by title",
            "description": "Searches The Movie Database (TMDB) for movies matching the given title.",
            "parameters": [
                {
                    "name": "title",
                    "in": "path",
                    "type": "string",
                    "required": True,
                    "description": "Title of the movie to search for",
                }
            ],
            "responses": {
                200: {
                    "description": "Successfully retrieved movie search results",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "results": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "title": {"type": "string"},
                                        "overview": {"type": "string"},
                                        "release_date": {"type": "string"},
                                        "vote_average": {"type": "number"},
                                    },
                                },
                            }
                        },
                    },
                },
                400: {"description": "Missing or invalid title parameter"},
                401: {"description": "Unauthorized"},
                500: {"description": "Internal server error"},
            },
        }
    )
    @jwt_required
    def get(self, title: str):

        if not title:
            return {"message": "Missing 'title' query parameter"}, 400
        try:
            results = search_movie(title)
            return {"results": results}, 200
        except Exception:
            return {"message": "Internal server error"}, 500


def async_request(async_function):
    """
    A function to send async requests in sync functions
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_function())
    loop.close()
    return result


def add_endpoints(api: Api) -> None:
    """
    Adds endpoints to the application's RESTful API.

    :param api: Flask-RESTful API object.
    """
    api.add_resource(Welcome, "/")
    api.add_resource(SearchMovie, "/movies/<string:title>")
    api.add_resource(
        MostPopular, "/movies/most_popular", "/movies/most_popular/<int:n>"
    )
    api.add_resource(MoviesWithSameGenres, "/movies/same_genres/<string:movie>")
    api.add_resource(MoviesWithSimilarRuntime, "/movies/similar_runtime/<string:movie>")
    api.add_resource(CreateUser, "/createUser")
    api.add_resource(Login, "/login")
    api.add_resource(FavoriteMovies, "/movies/favorite")
    api.add_resource(AddFavorite, "/movies/favorite/<int:movie_id>")
    api.add_resource(RemoveFavorite, "/movies/favorite/<int:movie_id>")


if __name__ == "__main__":
    MOVIE = "Harry Potter"
    search_result = search_movie(MOVIE)
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
