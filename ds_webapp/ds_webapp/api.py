"""
A file containing the app's API.
"""

from http.client import HTTPException
from typing import Tuple, List, Any, Dict
import asyncio

import asyncpg
from flasgger import swag_from
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse


from ds_webapp.authentication.authentication import create_jwt_token, jwt_required
from ds_webapp.api_client.tmdb_client import (
    get_movies_with_same_genres,
    get_movies_with_similar_runtime,
    get_popular_movies,
    search_movie,
    get_movie_details,
)
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
            "responses": {
                200: {
                    "description": "Returns a welcome message in a <span> tag.",
                    "content": {
                        "text/html": {
                            "example": "<span>Welcome to the movie list app!!</span>"
                        }
                    },
                }
            },
        }
    )
    def get(self):
        """
        Returns a welcome message wrapped in an HTML <span>.
        """
        html = "<span>Welcome to the movie list app!!</span>"
        response = jsonify(html)
        response.headers["Content-Type"] = "text/html"
        response.headers["Cache-Control"] = f"public, max-age={86400}"
        return response


class MostPopular(Resource):
    """
    A class to send requests related to the most popular movies.
    """

    @swag_from(
        {
            "tags": ["Popular"],
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
                401: {"description": "Unauthorized"},
                400: {
                    "description": "Bad Request",
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
        Returns a list of the n most popular movies (default = 1). Must be between 1 and 20.
        """
        try:
            if not 1 <= n <= 20:
                # Invalid value for 'n'. It should be between 1 and 20.
                response = jsonify({"error": "Bad Request"})
                response.headers["Cache-Control"] = "no-store"
                response.status_code = 400
                return response

            response = jsonify(get_popular_movies()[:n])
            response.headers["Cache-Control"] = f"public, max-age={3600}"
            return response
        # pylint: disable=locally-disabled, broad-exception-caught
        except Exception:
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response


class MoviesWithSameGenres(Resource):
    """
    A class to send requests related to movies with the same genres.
    """

    @swag_from(
        {
            "tags": ["Genres"],
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
                    "description": "Returns list of movies with same genres as the input movie.",
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
                401: {"description": "Unauthorized"},
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
        """
        try:
            movies = get_movies_with_same_genres(movie)

            if not movies:
                return {"error": "Not Found."}, 404

            response = jsonify(movies)
            response.headers["Cache-Control"] = f"public, max-age={86400}"
            return response
        # pylint: disable=locally-disabled, broad-exception-caught
        except Exception:
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response


class MoviesWithSimilarRuntime(Resource):
    """
    A class to send requests relates to movies with similar runtimes
    """

    @swag_from(
        {
            "tags": ["Runtime"],
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
                    "description": "Returns list of movies with same genres as the input movie.",
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
        """
        try:
            result = get_movies_with_similar_runtime(movie)

            if not result:
                return {"error": "Not Found."}, 404

            response = jsonify(result)
            response.headers["Cache-Control"] = f"public, max-age={3600}"
            return response

        except HTTPException as e:
            response = jsonify({"error": e})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 404
            return response
        # pylint: disable=locally-disabled, broad-exception-caught
        except Exception:
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response


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
        super(CreateUser, self).__init__()  #  pylint: disable=super-with-arguments

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
                201: {"description": "User created successfully"},
                409: {"description": "Username already exists"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def post(self):
        """
        Creates user and returns 201 OK if username is unique
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
                response = jsonify({"message": f"User {username} created successfully"})
                response.headers["Cache-Control"] = "no-store"
                response.status_code = 201
                return response

            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response

        except asyncpg.UniqueViolationError:
            response = jsonify({"error": "Username already exists"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 409
            return response
        except Exception:  # pylint: disable=broad-exception-caught
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response


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
        super(Login, self).__init__()  # pylint: disable=super-with-arguments

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
                200: {"description": "login successfull"},
                401: {"description": "Unauthorized (wrong username or password)"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def post(self):
        """
        Returns a bearer token if the credentials are valid
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
                        "username": username,
                    }
                )

                response = jsonify(token)
                response.headers["Cache-Control"] = f"public, max-age={3600*3}"
                return response

            response = jsonify({"error": "Unathorized"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 401
            return response
        except Exception:  # pylint: disable=broad-exception-caught
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response


class FavoriteMovies(Resource):
    """
    Get the list of favorite movies for the authenticated user
    """

    @swag_from(
        {
            "tags": ["Favorites"],
            "security": [{"BearerAuth": []}],
            "summary": "Get user's favorite movies",
            "description": "Retrieve list of movies marked as favorites by the authenticated user",
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
        """
        Returns a list of the users favorite movies
        """

        user_id = request.user["user_id"]
        favorites_table = Favorites(db=db)
        print("user id:", user_id)

        async def get_favorites():
            return await favorites_table.get_favorites(user_id=user_id)

        try:
            result = async_request(get_favorites)
            response = jsonify(
                {
                    "results": (
                        [get_movie_details(dict(row).get("movie_id")) for row in result]
                        if result
                        else []
                    )
                }
            )
            response.headers["Cache-Control"] = "no-store"
            return response
        except asyncpg.PostgresError:
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("error :", e)
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response


class AddFavorite(Resource):
    """
    Add a movie to favorites
    """

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
        """
        Adds movie to a users favorites, given a user id
        """
        user_id = request.user["user_id"]

        favorites_table = Favorites(db=db)

        async def like_movie():
            return await favorites_table.like_movie(user_id=user_id, movie_id=movie_id)

        try:
            async_request(like_movie)
            response = jsonify({"message": "OK"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 201
            return response
        except asyncpg.PostgresError:
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response
        except Exception:  # pylint: disable=broad-exception-caught
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response


class RemoveFavorite(Resource):
    """
    Remove movie from favorites
    """

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
        """
        Removes a movie from a users favorites
        """
        user_id = request.user["user_id"]
        favorites_table = Favorites(db=db)

        async def unlike_movie():
            return await favorites_table.unlike_movie(
                user_id=user_id, movie_id=movie_id
            )

        try:
            async_request(unlike_movie)
            response = jsonify({"message": "OK"})
            response.headers["Cache-Control"] = "no-store"
            return response
        except Exception:  # pylint: disable=broad-exception-caught
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response


class SearchMovie(Resource):
    """
    Search for movies by title using the MovieDB API
    """

    @swag_from(
        {
            "tags": ["Search"],
            "security": [{"BearerAuth": []}],
            "summary": "Search movies by title",
            "description": "Searches The Movie Database (TMDB) for movies "
            "matching the given title.",
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
        """
        A function to search for a movie given the title
        """

        if not title:
            return {"message": "Missing 'title' query parameter"}, 400
        try:
            results = search_movie(title)
            response = jsonify({"results": results})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 200
            return response
        except Exception:  # pylint: disable=broad-exception-caught
            response = jsonify({"message": "Internal server error"})
            response.headers["Cache-Control"] = "no-store"
            response.status_code = 500
            return response


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
    api.add_resource(Welcome, "/", "/movies")
    api.add_resource(SearchMovie, "/movies/<string:title>")
    api.add_resource(
        MostPopular, "/movies/most_popular", "/movies/most_popular/<int:n>"
    )
    api.add_resource(MoviesWithSameGenres, "/movies/same_genres/<string:movie>")
    api.add_resource(MoviesWithSimilarRuntime, "/movies/similar_runtime/<string:movie>")
    api.add_resource(CreateUser, "/user")
    api.add_resource(Login, "/login")
    api.add_resource(FavoriteMovies, "/movies/favorite")
    api.add_resource(AddFavorite, "/movies/favorite/<int:movie_id>")
    api.add_resource(RemoveFavorite, "/movies/favorite/<int:movie_id>")
