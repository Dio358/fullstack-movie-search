"""This module defines the main application for ds_webapp.

It sets up the web framework, routes, and initializes the necessary services.
"""

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_restful import Api

import ds_webapp.api

# load environment variables
load_dotenv()

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
            "description": "Enter your Bearer token in the format 'Bearer <your-token-here>'",
        }
    },
    "security": [{"BearerAuth": []}],
}

swagger = Swagger(app)
ds_webapp.api.add_endpoints(api)

def start():
    """
    Start Application
    """
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    start()
