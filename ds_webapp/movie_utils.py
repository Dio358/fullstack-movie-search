"""
    A file with utils to create and parse responses
"""
from ds_webapp.schemas import Movie


def create_movie_list(movie_list: list[Movie], length: int):
     """
     A function which takes creates a list of the 'length' most popular movies
     :param movie_list: list of movies
     :param length: desired length of the list
     :return:
     """
     return  [{"rank": i + 1, "title": movie_list[i].title}for i in range(length)]