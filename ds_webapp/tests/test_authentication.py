"""
A file the test authentication.py
"""

from ds_webapp.authentication.authentication import create_jwt_token, verify_jwt_token


def test_jwt_token_happy_day():
    """
    A function that tests jwt token creation and verification
    """
    payload = {
        "user_id": 0,
        "username": "JohnDoe123",
    }
    token = create_jwt_token(payload)
    print("JWT TOKEN:", token)
    print("... verifying token ...")

    assert verify_jwt_token(token)
    assert not verify_jwt_token("token")


def test_jwt_required_decorator(test_app):
    """
    A function to test jwt token verification wrapper
    """
    client = test_app.test_client()

    payload = {"user_id": 42, "username": "test"}
    token = create_jwt_token(payload)

    response = client.get("/protected")
    assert response.status_code == 401

    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Access granted"
