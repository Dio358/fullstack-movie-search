"""
A file containing a class for each of the database tables and methods to query them
"""

import bcrypt
from ds_webapp.database.connect import Database


class Users:
    """
    A class representing the users(id, username, password)
    """
    def __init__(self, db: Database):
        self.columns = "username, password"
        self.db = db
    def add_user(self, username: str, password: str) -> None:
        """
        Adds user to table users
        """
        sql = f"""INSERT INTO users({self.columns})
             VALUES(%s, %s) RETURNING id;"""
        params = [username, Hasher.hash_password(password)]
        return self.db.query(sql=sql, params=params)[0][0]

    def get_user(self, user_id: int):
        """
        Returns user with given id
        """
        sql = "SELECT * FROM users WHERE id = %s"
        return self.db.query(sql=sql, params=[user_id])
    def get_user_id(self, username: str, password: str):
        """
        Returns user_id based on username and password
        """
        sql = "SELECT * FROM users WHERE username = %s"
        search_result = self.db.query(sql=sql, params=[username])
        for user_id, username, hashed_password in search_result:
            if Hasher.verify_password(hashed_password=hashed_password.encode('utf-8'),password=password):
                return user_id

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
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        except ValueError:
            return False
    
class Favorites:
    """
    A class representing the favorites (movie_id, user_id)
    """
    def __init__(self, db: Database):
        self.columns = "movie_id, user_id"
        self.db = db

    def like_movie(self, movie_id: int, user_id: int) -> None:
        """
        Adds (movie_id, user_id) to the favorites table
        """
        sql = f"""INSERT INTO favorites({self.columns})
                  VALUES(%s, %s);"""
        params = [movie_id, user_id]
        return self.db.query(sql=sql, params=params)

    def unlike_movie(self, movie_id: int, user_id: int) -> None:
        """
        Removes (movie_id, user_id) from the favorites table
        """
        sql = """
                DELETE FROM favorites
                WHERE movie_id = %s AND user_id = %s;
              """
        return self.db.query(sql=sql, params=[movie_id, user_id])

    def get_favorites(self, user_id: int) -> list[dict]:
        """
        Returns all movies liked by the user with user_id
        """
        sql = """
                SELECT * FROM favorites
                WHERE user_id = %s
              """
        return self.db.query(sql=sql, params=[user_id])
