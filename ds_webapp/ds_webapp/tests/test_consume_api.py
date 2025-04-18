"""
Tests for the API showcasing the following functionalities:

1. List the first n popular movies.
2. Given a movie, return a list of movies with all genres in common.
3. Given a movie, return movies with a similar runtime (+/- 10 minutes).
4. Compare average scores visually (done via UI only at localhost:3000, as was approved via mail).
5. Favorite/unfavorite a movie and retrieve favorite movies list (test_favorites).
"""

import pytest
from ds_webapp.database.tables import Favorites, Users
from ds_webapp.api_client.tmdb_client import (
    get_movies_with_same_genres,
    get_movies_with_similar_runtime,
    get_popular_movies,
    search_movie,
)


@pytest.fixture
def movie():
    """
    Returns the movie to use in the tests.
    """
    return "Harry Potter and the Philosopher's Stone"


def print_movie_titles(movie_list: list[dict[str, str | int]]):
    """
    Prints the titles of the movies in the given list.
    """
    if not movie_list:
        print("No movies found.")
        return
    for m in movie_list:
        title = m.get("title")
        print(f"  - {title}")


# ** Functionality 1: List the first n popular movies **
def test_popular_movies():
    """
    Tests retrieval of the n most popular movies.
    """
    print("\n===== Functionality 1: Popular Movies =====")
    movies = get_popular_movies()
    n = 20

    print(f"\nTop {n} most popular movies:")
    print_movie_titles(movie_list=movies[:n])

    n_half = int(n / 2)
    print(f"\nTop {n_half} most popular movies:")
    print_movie_titles(movie_list=movies[:n_half])


# ** Functionality 2: Return movies with the same genres **
def test_genres_in_common(movie: str):
    """
    Tests finding movies that share all genres with a given movie.
    """
    print("\n===== Functionality 2: Movies with Same Genres =====")
    print(f"Searching for movies that share all genres with '{movie}'...\n")

    result = get_movies_with_same_genres(movie)
    assert result is not None

    print("Movies with matching genres:")
    print_movie_titles(result)


# ** Functionality 3: Return movies with similar runtime (+/- 10 min) **
def test_genres_similar_runtime(movie: str):
    """
    Tests finding movies with a similar runtime to a given movie.
    """
    print("\n===== Functionality 3: Movies with Similar Runtime =====")
    print(f"Searching for movies with a runtime within ±10 minutes of '{movie}'...\n")

    result = get_movies_with_similar_runtime(movie)
    assert result is not None

    print("Movies with similar runtimes:")
    print_movie_titles(result)


# ** Functionality 5: Favorite/unfavorite functionality **
@pytest.mark.asyncio
async def test_favorites(db, movie):
    """
    Tests the ability to favorite/unfavorite movies and retrieve favorites.
    """
    print("\n===== Functionality 5: Favorite/Unfavorite Movies =====")

    user_table = Users(db=db)
    favorites_table = Favorites(db=db)
    username = "john doe"
    password = "password"
    user_id = None

    try:
        print("\nCreating test user...")
        user_id = await user_table.add_user(username=username, password=password)

        uid_from_table = await user_table.get_user_id(
            username=username, password=password
        )
        assert user_id == uid_from_table
        print(f"User '{username}' created with ID {user_id}.")

        print(f"\nSearching for movie '{movie}' to favorite...")
        search_result = search_movie(movie)
        assert search_result is not None
        movie_id = search_result[0].get("id")

        print(f"\nAdding '{movie}' (ID: {movie_id}) to favorites...")
        await favorites_table.like_movie(movie_id=movie_id, user_id=user_id)

        favorites = await favorites_table.get_favorites(user_id=user_id)
        assert any(
            f["movie_id"] == movie_id and f["user_id"] == user_id for f in favorites
        )
        print(f"'{movie}' has been added to favorites for user '{username}'.")

        print(f"\nRemoving '{movie}' from favorites...")
        await favorites_table.unlike_movie(movie_id=movie_id, user_id=user_id)

        favorites_after_delete = await favorites_table.get_favorites(user_id=user_id)
        assert not favorites_after_delete
        print(f"'{movie}' successfully removed from favorites.")

    finally:
        print("\nCleaning up test data...")
        await favorites_table.unlike_movie(movie_id=movie_id, user_id=user_id)
        if user_id:
            await user_table.delete_user(user_id=user_id)
        print("Cleanup complete.")
