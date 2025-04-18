"""
A file for testing app.py
"""


def test_env(api_url, api_key):
    """Test to ensure environment variables are loaded correctly"""
    assert api_key is not None
    assert api_url is not None
