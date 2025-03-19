"""
A file for testing app.py
"""
import responses
from ds_webapp.app import API_URL, API_KEY
from ds_webapp.tests.fixtures import client


def test_env():
    """Test to ensure environment variables are loaded correctly"""
    assert API_KEY is not None
    assert API_URL is not None

@responses.activate
def test_authenticate(client):
    """Test the /authenticate route with mocked external API."""
    # Mock the external API response
    mock_response = {"status": "authenticated"}
    responses.add(
        responses.GET,
        API_URL,
        json=mock_response,
        status=200
    )

    # Make the request to our app
    response = client.get("/authenticate")

    # Assert the response
    assert response.status_code == 200

    # Check that the request to the external API was made with correct headers
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers["Authorization"] == API_KEY