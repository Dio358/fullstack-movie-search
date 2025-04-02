"""
A file with database connection tests
"""
import pytest
from ..database.connect import Database

@pytest.mark.asyncio
async def test_connection():
    """
    A function to test the database connection
    """
    db = Database()
    await db.connect()

    sql_create = """
        CREATE TABLE IF NOT EXISTS test_users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT
        );
    """
    sql_drop = "DROP TABLE IF EXISTS test_users;"

    try:
        result = await db.query(sql=sql_create, params=[])
        assert not result
    finally:
        await db.query(sql=sql_drop, params=[])
        await db.close()


@pytest.mark.asyncio
async def test_insert():
    """
    A function to test insert and select from the database
    """
    db = Database()
    await db.connect()

    try:
        sql_create = """
        CREATE TABLE IF NOT EXISTS test_users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT
        );
        """
        result = await db.query(sql=sql_create, params=[])
        assert not result

        insert = """
            INSERT INTO test_users(id, name, password) VALUES ($1, $2, $3);
            """
        insert_params = [0, "john doe", "password"]
        await db.query(sql=insert, params=insert_params)

        select = """
                    SELECT * from test_users;
                """
        select_result = await db.query(sql=select, params=[])
        assert any(
            row["id"] == 0 and row["name"] == "john doe" and row["password"] == "password"
            for row in select_result
        )

        delete = """
                    DELETE from test_users
                    WHERE id = $1;
                """
        await db.query(sql=delete, params=[0])

        select_result_after_delete = await db.query(sql=select, params=[])
        print(select_result_after_delete)
        assert not select_result_after_delete

    finally:
        sql_drop = "DROP TABLE IF EXISTS test_users;"
        await db.query(sql=sql_drop, params=[])
        await db.close()
