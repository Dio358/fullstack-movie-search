"""
A file containing a class for each of the database tables and methods to query them
"""

import bcrypt
from ds_webapp.database.connect import Database


class Users:
    """
    A class representing the users(id, name, password)
    """
    def __init__(self, db: Database):
        self.columns = "id, name, password"
        self.db = db
    def add_user(self, username: str, password: str) -> None:
        """
        Adds user to table users
        """
        sql = """INSERT INTO users(name, password)
             VALUES(%s, %s) RETURNING id;"""
        params = [username, Hasher.hash_password(password)]
        return self.db.query(sql=sql, params=params)[0][0]

    def get_user(self, user_id: int):
        """
        Returns user with given id
        """
        sql = "SELECT * FROM users WHERE id = %s"
        return self.db.query(sql=sql, params=[user_id])
        
    def get_users(self):
        """
        Returns a list of all users in db
        """
        sql = """SELECT * FROM users"""
        return self.db.query(sql=sql, params=[])
    def delete_user(self, user_id: int):
        """
        A function to delete a user based on his user_id
        """
        delete = """
                    DELETE from users
                    WHERE id = %s;
                """
        self.db.query(sql=delete, params=[user_id])


class Hasher:
    """
    A class containing hashing methods
    """
    @staticmethod
    def hash_password(password: str):
        """
        A function that returns a hashed password (as a string)
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8') , salt).decode("utf-8")
    @staticmethod
    def verify_password(hashed_password: bytes, password: str) -> bool:
        """
        A function to verify passwords
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

