"""
A containing the database connnection and query class
"""

import os
import asyncio
import asyncpg

class Database:
    """
    A class for interacting with a PostgreSQL database using asyncpg.
    """

    def __init__(self, max_retries=2, retry_delay=1, debug_mode=False):
        """
        Initialize parameters
        """
        self.conn = None
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.debug_mode = debug_mode

    async def connect(self):
        """
        Attempt to connect to the database with retries.
        """
        for attempt in range(self.max_retries):
            try:
                self.conn = await asyncpg.connect(
                    user=os.getenv("POSTGRES_USER", "pgres"),
                    password=os.getenv("POSTGRES_PASSWORD", "pgres"),
                    database=os.getenv("POSTGRES_DB", "pgres"),
                    host=os.getenv("POSTGRES_HOST", "db"),
                    port=5432,
                    timeout=5.0
                )
                print(f"Database connection successful on attempt {attempt + 1}")
                return
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise RuntimeError(f"Failed to connect to database after {self.max_retries} attempts")

    async def query(self, sql: str, params: list = None):
        """
        Run a SQL query with optional parameters. Returns all rows or False.
        """
        if not self.conn or self.conn.is_closed():
            await self.connect()

        try:
            result = await self.conn.fetch(sql, *(params or []))
            return result if result else False
        except Exception as e:
            print(f"Database query error: {e}")
            raise e

    async def close(self):
        """
        Close the DB connection.
        """
        if self.conn:
            await self.conn.close()
            print("Database connection closed")
