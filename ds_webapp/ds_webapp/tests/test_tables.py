"""
A file to test tables.py
"""

import pytest
from ds_webapp.database.tables import Users, Hasher, Favorites


@pytest.mark.asyncio
async def test_users(db):
    """
    A function to test the users table access class methods
    """
    user_table = Users(db=db)
    username = "john doe"
    password = "password"
    user_id = None

    try:
        user_id = await user_table.add_user(username=username, password=password)

        user = await user_table.get_user(user_id)
        assert user
        assert user[0]["id"] == user_id
        assert user[0]["username"] == username
        assert Hasher.verify_password(
            password=password, hashed_password=user[0]["password"].encode("utf-8")
        )

        uid_from_table = await user_table.get_user_id(
            username=username, password=password
        )
        assert user_id == uid_from_table

        await user_table.delete_user(user_id=user_id)

        user = await user_table.get_user(user_id)
        assert not user

        uid = await user_table.get_user_id(username=username, password=password)
        assert not uid

    finally:
        if user_id:
            await user_table.delete_user(user_id=user_id)


def test_password_hasher():
    """
    A function to test the password hasher
    """
    h = Hasher()
    hashed_password: bytes = h.hash_password("password")
    assert h.verify_password(
        password="password", hashed_password=hashed_password.encode("utf-8")
    )


@pytest.mark.asyncio
async def test_favorites(db):
    """
    A function to test the favorites table access class methods
    """
    user_table = Users(db=db)
    favorites_table = Favorites(db=db)
    username = "john doe"
    password = "password"
    movie_id = 0
    user_id = None

    try:
        user_id = await user_table.add_user(username=username, password=password)

        uid_from_table = await user_table.get_user_id(
            username=username, password=password
        )
        assert user_id == uid_from_table

        await favorites_table.like_movie(movie_id=movie_id, user_id=user_id)
        favorites = await favorites_table.get_favorites(user_id=user_id)
        assert any(
            f["movie_id"] == movie_id and f["user_id"] == user_id for f in favorites
        )

        await favorites_table.unlike_movie(movie_id=movie_id, user_id=user_id)
        favorites_after_delete = await favorites_table.get_favorites(user_id=user_id)
        assert not favorites_after_delete

    finally:
        await favorites_table.unlike_movie(movie_id=movie_id, user_id=user_id)
        if user_id:
            await user_table.delete_user(user_id=user_id)
