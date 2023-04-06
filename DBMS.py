import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query, values):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


create_competitors_table = """
CREATE TABLE IF NOT EXISTS competitors (
  id INTEGER PRIMARY KEY,
  name TEXT,
  surname TEXT,
  patronymic TEXT,
  age INTEGER,
  weight INTEGER,
  status TEXT
);
"""


def add_id_in_competitors(connection, user_id):
    add_id_in_competitors = """
    INSERT INTO
        competitors (id)
    VALUES
        (?);
    """
    
    execute_query(connection, add_id_in_competitors, user_id)