"""This module defines the main application for ds_webapp.

It sets up the web framework, routes, and initializes the necessary services.
"""

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS

import ds_webapp.api

# load environment variables
load_dotenv()

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=False,
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

api = Api(app)

# Configuring Swagger
app.config["SWAGGER"] = {
    "title": "Movie List API",
    "uiversion": 3,
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: Bearer <JWT token> (including 'Bearer ' prefix)",
        }
    },
    "security": [{"BearerAuth": []}],
}


@app.before_request
def log_request_info():
    print(f"Method: {request.method}")
    print(f"Headers: {dict(request.headers)}")


swagger = Swagger(app)
ds_webapp.api.add_endpoints(api)


def start():
    """
    Start Application
    """
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    start()
