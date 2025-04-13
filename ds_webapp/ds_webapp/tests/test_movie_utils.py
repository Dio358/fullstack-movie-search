"""
A file for testing utils.py
"""

from ds_webapp.api_client.utils import create_movie_list, create_ranked_movie_list


def test_create_movie_list(movie_list_example):
    """
    A function that tests the create_movie_list function, using an example list
    """
    assert "title" in create_movie_list(movie_list_example)[0]


def test_create_ranked_movie_list(movie_list_example):
    """
    A function that tests the create_ranked_movie_list function, using an example list
    """
    for i in range(20):
        assert i == len(create_ranked_movie_list(movie_list_example, i))

    assert "title" in create_ranked_movie_list(movie_list_example, 1)[0]
    assert "rank" in create_ranked_movie_list(movie_list_example, 1)[0]
