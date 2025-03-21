"""
A file containing the app's api
"""

from flasgger import swag_from
from flask import Response
from flask_restful import Resource, Api
from ds_webapp.consume_api.consume_api import get_movies_list


class Welcome(Resource):
    """
    A class welcoming the user to the webpage
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
        returns a welcome message
        :return: Response
        """
        return Response(
            {
                "Welcome to the movie list app!! Please go to apidocs to see the endpoint swagger!"
            },
            200,
        )


class Movies(Resource):
    """A class to send requests related to movies"""

    @swag_from(
        {
            "tags": ["Movies"],
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
        returns a welcome message
        :return: Response
        """
        return Response(
            {
                "Welcome to the movie list app!! Please go to apidocs to see the endpoint swagger!"
            },
            200,
        )


class MostPopular(Movies):
    """A class to send requests related to movies"""

    @swag_from(
        {
            "tags": ["Movies"],
            "parameters": [
                {
                    "name": "n",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                    "description": "The number of movies to retrieve (1-20)",
                }
            ],
            "responses": {
                200: {
                    "description": "A status code 200 means successful and returns a list of movies.",
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
                    "description": "Invalid value for 'n'. It should be between 1 and 20.",
                },
            },
        }
    )
    def get(self, n: int = 1) -> Response | tuple[Response, int]:
        """
        Request a list of the n most popular movies.
        :param n: an int
        :precondition: 1 <= n <= 20
        :return: a JSON list of movies
        """
        if not 1 <= n <= 20:
            return Response(
                {"error": "Invalid value for 'n'. It should be between 1 and 20."}, 400
            )

        return get_movies_list(n)


def add_endpoints(api: Api) -> None:
    """
    Adds endpoints to app's restful API
    :param api: app's restful api
    :return: None
    """
    api.add_resource(Welcome, "/")
    api.add_resource(Movies, "/movies")
    api.add_resource(
        MostPopular, "/movies/most_popular", "/movies/most_popular/<int:n>"
    )
