"""This module defines the main application for ds_webapp.

It sets up the web framework, routes, and initializes the necessary services.
"""
import os
from dotenv import load_dotenv
from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests

from ds_webapp.movie_utils import create_movie_list
from ds_webapp.schemas import Movie

# load environment variables
load_dotenv()

# setting API url and key
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
api = Api(app)

# Configuring Swagger
app.config["SWAGGER"] = {
    "title": "My API",
    "uiversion": 3,
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your Bearer token in the format 'Bearer <your-token-here>'"
        }
    },
    "security": [{"BearerAuth": []}]
}

swagger = Swagger(app)


class Movies(Resource):
    """A class to send requests related to movies"""
    @swag_from(
        {
            "parameters": [
                        {
                            "name": "n",
                            "in": "query",
                            "type": "integer",
                            "required": True,
                            "description": "The length of the list of requested movies"
                        }
                    ],
            "responses": {
                200: {
                    "description": "A status code 200 means successful and returns a message.",
                    "content": {
                        "application/json": {
                            "examples": {
                                "example1": {
                                    "summary": "Successful response",
                                    "value": [{"title": "Movie 1"}, {"title": "Movie 2"}],
                                }
                            }
                        }
                    },
                }
            }
        }
    )

    def get(self):
        """
        Request a list of the n most popular movies,
        :param n: an int
        :precondition: 1 <= n <= 20
        :return:
        """

        n = request.args.get("n", default=1, type=int)

        headers = {
            "accept": "application/json",
            "Authorization": API_KEY
        }

        params = {
            "language": "en-US",
            "page": n
        }

        response = requests.get(f"{API_URL}/movie/popular", headers=headers, params=params)

        if response.status_code == 200:
            return jsonify(create_movie_list(movie_list=[Movie.model_validate(movie) for movie in response.json()["results"]], length=n))

        return jsonify({"error": str(response.status_code), "message": response.text}), response.status_code



api.add_resource(Movies, "/movies")

if __name__ == "__main__":
    app.run(debug=True)