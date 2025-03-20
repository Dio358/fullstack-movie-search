"""
A file for testing app.py
"""

import responses


def test_env(api_url, api_key):
    """Test to ensure environment variables are loaded correctly"""
    assert api_key is not None
    assert api_url is not None


@responses.activate
def test_authenticate(client, api_url, api_key):
    """Test the /authenticate route with mocked external API."""
    # Mock the external API response
    mock_response = {"status": "authenticated"}
    responses.add(responses.GET, api_url, json=mock_response, status=200)

    # Make the request to our app
    response = client.get("/authenticate")

    # Assert the response
    assert response.status_code == 200

    # Check that the request to the external API was made with correct headers
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers["Authorization"] == api_key
