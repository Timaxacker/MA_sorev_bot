import sqlite3
from sqlite3 import Error



def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query_values(connection, query, values):
    global error
    error = False
    
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
    except Error as e:
        error = True
        print(f"The error '{e}' occurred")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
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
  surname TEXT,
  name TEXT,
  patronymic TEXT,
  sex TEXT,
  age INTEGER,
  weight INTEGER,
  status TEXT
);
"""

delete_comment = "DELETE FROM competitors WHERE id > 0"

select_competitors = "SELECT * from competitors"



def add_information_in_competitors(connection, info):
    add_information_in_competitors_query = """
    INSERT INTO
        competitors (id, surname, name, patronymic, sex, age, weight, status)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?);
    """
    
    execute_query_values(connection, add_information_in_competitors_query, info)