"""
A file to test tables.py
"""
from ds_webapp.database.tables import Users, Hasher, Favorites

def test_users(db):
    """
    A function to test the users table access class methods
    """
    user_table = Users(db=db)
    username = "john doe"
    password = "password"
    user_id = None

    try:
        user_id = user_table.add_user(username=username, password=password)

        user = user_table.get_user(user_id)
        assert user is not None
        assert user[0][0] == user_id
        assert user[0][1] == username
        assert Hasher.verify_password(password=password, hashed_password=user[0][2].encode('utf-8'))

        uid_from_table = user_table.get_user_id(username=username, password=password)
        assert user_id == uid_from_table

        user_table.delete_user(user_id=user_id)

        user = user_table.get_user(user_id)
        assert not user
    finally:
        if user_id:
            user_table.delete_user(user_id=user_id)

def test_password_hasher():
    """
    A function to test the password hasher
    """
    h = Hasher()
    hashed_password: bytes = h.hash_password("password")
    assert h.verify_password(password="password", hashed_password=hashed_password.encode('utf-8'))  

def test_favorites(db):
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
        user_id = user_table.add_user(username=username, password=password)

        uid_from_table = user_table.get_user_id(username=username, password=password)
        assert user_id == uid_from_table

        favorites_table.like_movie(movie_id=movie_id, user_id=user_id)    
        favorites = favorites_table.get_favorites(user_id=user_id)
        assert (movie_id, user_id) in favorites

        favorites_table.unlike_movie(movie_id=movie_id, user_id=user_id)
        favorites_after_delete = favorites_table.get_favorites(user_id=user_id)
        assert (movie_id, user_id) not in favorites_after_delete

    finally:
        favorites_table.unlike_movie(movie_id=movie_id, user_id=user_id)
        if user_id:
            user_table.delete_user(user_id=user_id)
