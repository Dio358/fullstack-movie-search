"""
A containing the database connnection and query class
"""
import os
import time
import psycopg2
from psycopg2 import OperationalError

class Database:
    """
    A class for interacting with the database with improved connection handling
    """
    def __init__(self, max_retries=2, retry_delay=1, debug_mode=False):
        """
        Initialize database connection with retry mechanism
        
        :param max_retries: Maximum number of connection retry attempts
        :param retry_delay: Delay between retry attempts in seconds
        """
        self.conn = None
        self.debug_mode =  debug_mode
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._connect()

    def _connect(self):
        """
        Attempt to connect to the database with retries
        """
        for attempt in range(self.max_retries):
            try:
                # Use environment variables or default dev settings
                self.conn = psycopg2.connect(
                    dbname=os.getenv("POSTGRES_DB", "pgres"),
                    user=os.getenv("POSTGRES_USER", "pgres"),
                    password=os.getenv("POSTGRES_PASSWORD", "pgres"),
                    host=os.getenv("POSTGRES_HOST", "db"),
                    port = 5432,
                    connect_timeout=5  # 5-second connection timeout
                )
                if not self.debug_mode:
                    self.conn.autocommit = True
                print(f"Database connection successful on attempt {attempt + 1}")
                return
            except (psycopg2.Error, OperationalError) as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise RuntimeError(f"Failed to connect to database after {self.max_retries} attempts")

    def query(self, sql: str, params: list[str|int] = None):
        """
        A function to query the DB with additional error handling
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, params or [])
                if cur.description:  # if SELECT
                    return cur.fetchall()
            return "NOT FOUND"
        except psycopg2.Error as e:
            print(f"Database query error: {e}")
            raise

    def close(self):
        """
        A function to close the DB connection
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def rollback(self):
        """
        A function to rollback transactions
        """
        if self.conn:
            self.conn.rollback()
            print("Transaction rolled back")

