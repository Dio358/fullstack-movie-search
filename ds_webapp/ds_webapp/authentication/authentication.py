"""
A file for JWT authentication
"""

from functools import wraps
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import request
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_jwt_token(payload: dict) -> str:
    """
    Create and return a JWT token
    """
    payload["exp"] = datetime.now() + timedelta(hours=3)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt_token(token):
    """
    A function that returns wether token is valid
    """
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


def jwt_required(func):
    """
    A wrapper function for requests,
    verifies jwt tokens and stores the user_id and username in the request
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return {"error": auth_header}, 401
        token = auth_header.split(" ")[1]
        try:
            user_data = verify_jwt_token(token)
            request.user = user_data
        except ValueError as e:
            return {"error": str(e)}, 401
        return func(*args, **kwargs)

    return wrapper
