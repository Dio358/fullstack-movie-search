"""
A file for testing app.py
"""

import pytest
from ds_webapp import app


@pytest.fixture
def items():
    """Fixture to provide an instance of Items"""
    return app.Items()


def test_get(items):
    """Test that the class method Items get() returns something"""
    assert items.get() is not None
