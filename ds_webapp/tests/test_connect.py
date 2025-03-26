"""
A file with database connection tests
"""
from ..database.connect import Database

def test_connection(db: Database):
    """
    A function to test the database connection
    """
    sql_create = """
        CREATE TABLE IF NOT EXISTS test_users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT
        );
    """
    sql_drop = "DROP TABLE IF EXISTS test_users;"

    try:
        result = db.query(sql=sql_create, params=[])
        assert result == "NOT FOUND"
    finally:
        db.query(sql=sql_drop, params=[])

def test_insert(db: Database):
    """
    A function to test the database connection
    """
    try:
        sql_create = """
        CREATE TABLE IF NOT EXISTS test_users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT
        );
        """
        result = db.query(sql=sql_create, params=[])
        assert result == "NOT FOUND"

        insert = """
            INSERT INTO test_users(id, name, password) VALUES (%s, %s, %s);
            """
        insert_params = [0, "john doe", "password"]
        db.query(sql=insert, params=insert_params)

        select = """
                    SELECT * from test_users;
                """
        select_result = db.query(sql=select, params=[])
        assert tuple(insert_params) in select_result

        delete = """
                    DELETE from test_users
                    WHERE id = %s;
                """

        db.query(sql=delete, params=[0])
        select_result_after_delete = db.query(sql=select, params=[])
        assert tuple(insert_params) not in select_result_after_delete

    finally:
        sql_drop = "DROP TABLE IF EXISTS test_users;"
        db.query(sql=sql_drop, params=[])
        db.rollback()
