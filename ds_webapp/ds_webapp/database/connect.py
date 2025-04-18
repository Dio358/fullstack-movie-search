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

    def __init__(self, debug_mode=False):
        """
        Initialize parameters
        """
        self.conn = None
        self.max_retries = 2
        self.retry_delay = 1
        self.debug_mode = debug_mode

    async def connect(self):
        """
        Attempt to connect to the database with retries.
        """
        for attempt in range(self.max_retries):
            try:
                self.conn = await asyncpg.connect(
                    user=os.getenv("POSTGRES_USER"),
                    password=os.getenv("POSTGRES_PASSWORD"),
                    database=os.getenv("POSTGRES_DB"),
                    host=os.getenv("POSTGRES_HOST"),
                    port=5432,
                    timeout=5.0,
                )
                return
            except asyncpg.PostgresConnectionError as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise e

    async def query(self, sql: str, params: list = None):
        """
        Run a SQL query with optional parameters. Returns all rows or False.
        """
        if not self.conn or self.conn.is_closed():
            await self.connect()

        try:
            result = await self.conn.fetch(sql, *(params or []))
            return result if result else False

        finally:
            await self.conn.close()

    async def close(self):
        """
        Close the DB connection.
        """
        if self.conn:
            await self.conn.close()
