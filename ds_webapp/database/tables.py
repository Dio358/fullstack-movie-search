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

    async def add_user(self, username: str, password: str) -> int:
        """
        Adds user to table users
        """
        sql = f"""INSERT INTO users({self.columns})
                  VALUES($1, $2)
                  RETURNING id;"""
        params = [username, Hasher.hash_password(password)]
        result = await self.db.query(sql=sql, params=params)
        return result[0]["id"] if result else False

    async def get_user(self, user_id: int):
        """
        Returns user with given id
        """
        sql = "SELECT * FROM users WHERE id = $1"
        return await self.db.query(sql=sql, params=[user_id])

    async def get_user_id(self, username: str, password: str):
        """
        Returns user_id based on username and password
        """
        sql = "SELECT * FROM users WHERE username = $1"
        search_result = await self.db.query(sql=sql, params=[username])

        if not search_result:
            return False
        for user in search_result:
            if Hasher.verify_password(
                hashed_password=user["password"].encode("utf-8"),
                password=password,
            ):
                return user["id"]

    async def get_users(self):
        """
        Returns a list of all users in db
        """
        sql = "SELECT * FROM users"
        return await self.db.query(sql=sql)

    async def delete_user(self, user_id: int):
        """
        A function to delete a user based on their user_id
        """
        delete = """
                 DELETE FROM users
                 WHERE id = $1;
                """
        return await self.db.query(sql=delete, params=[user_id])


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
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(hashed_password: bytes, password: str) -> bool:
        """
        A function to verify passwords
        """
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
        except ValueError:
            return False


class Favorites:
    """
    A class representing the favorites (movie_id, user_id)
    """

    def __init__(self, db: Database):
        self.columns = "movie_id, user_id"
        self.db = db

    async def like_movie(self, movie_id: int, user_id: int) -> None:
        """
        Adds (movie_id, user_id) to the favorites table
        """
        sql = f"""INSERT INTO favorites({self.columns})
                  VALUES($1, $2);"""
        params = [movie_id, user_id]
        return await self.db.query(sql=sql, params=params)

    async def unlike_movie(self, movie_id: int, user_id: int) -> None:
        """
        Removes (movie_id, user_id) from the favorites table
        """
        sql = """
                DELETE FROM favorites
                WHERE movie_id = $1 AND user_id = $2;
              """
        return await self.db.query(sql=sql, params=[movie_id, user_id])

    async def get_favorites(self, user_id: int) -> list[dict]:
        """
        Returns all movies liked by the user with user_id
        """
        sql = """
                SELECT * FROM favorites
                WHERE user_id = $1
              """
        return await self.db.query(sql=sql, params=[user_id])
