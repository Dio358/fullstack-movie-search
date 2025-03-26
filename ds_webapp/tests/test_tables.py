"""
A file to test tables.py
"""
from ds_webapp.database.tables import Users, Hasher

def test_users(db):
    """
    A function to test the users table
    """
    user_table = Users(db=db)
    try:
        user_id = user_table.add_user("john doe", "password")

        user = user_table.get_user(user_id)
        assert user is not None
        assert user[0][0] == user_id
        assert user[0][1] == "john doe"
        assert Hasher.verify_password(password="password", hashed_password=user[0][2].encode('utf-8'))

        user_table.delete_user(user_id=user_id)

        user = user_table.get_user(user_id)
        assert not user  # should be empty list
    finally:
        db.rollback()


def test_password_hasher():
    """
    A function to test the password hasher
    """
    h = Hasher()
    hashed_password: bytes = h.hash_password("password")
    assert h.verify_password(password="password", hashed_password=hashed_password.encode('utf-8'))
    