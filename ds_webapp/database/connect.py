"""
This script initializes the required tables in the database when starting up the container.
"""

# db.py
import os
import psycopg2

class Database:
    """
    A class for interacting with the database
    """
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT"),
        )
        self.conn.autocommit = True

    def query(self, sql, params=None):
        """
        A function to query the DB
        """
        with self.conn.cursor() as cur:
            cur.execute(sql, params or [])
            if cur.description:  # if SELECT
                return cur.fetchall()
        return "NOT FOUND"

    def close(self):
        """
        A function to close the DB
        """
        self.conn.close()
        