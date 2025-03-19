"""
A file for testing movie_utils.py
"""

from ds_webapp.movie_utils import create_movie_list
from ds_webapp.tests.fixtures import movie_list_example


def test_create_movie_list(movie_list_example):
    for i in range(20):
        assert i == len(create_movie_list(movie_list_example, i))
    assert "title", "rank" in create_movie_list(movie_list_example, 1)[0]