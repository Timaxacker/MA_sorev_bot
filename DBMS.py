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


create_ages_table = """
CREATE TABLE IF NOT EXISTS ages (
  id INTEGER PRIMARY KEY,
  interval TEXT
);
"""

create_ages_intervals = """
INSERT INTO
  ages (id, interval)
VALUES
  (0, '4-5');
"""


create_statuses_table = """
CREATE TABLE IF NOT EXISTS statuses (
  id INTEGER PRIMARY KEY,
  interval TEXT
);
"""

create_statuses_intervals = """
INSERT INTO
  statuses (id, interval)
VALUES
  (0, 'Новичок');
"""


delete_comment = "DELETE FROM competitors WHERE id >= 0"


select_competitors = "SELECT * from competitors"


select_competitors_in_categories = """
SELECT
    competitors.id,
    competitors.sex,
    competitors.age,
    competitors.weight,
    competitors.status
FROM
    competitors
"""



def add_information_in_competitors(connection, info):
    add_information_in_competitors_query = """
    INSERT INTO
        competitors (id, surname, name, patronymic, sex, age, weight, status)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?);
    """
    
    execute_query_values(connection, add_information_in_competitors_query, info)



    

surnames = ["Хуеглотов", "Лазарев", "Белобородов", "Пидоро", "Ващенко"]
names = ["Валера", "Гоша", "Серёжа", "Виктор", "Олежа"]
patronymics = ["Алексеевич", "Михалыч", "Игнатич", "Буратиныч", "Виcсарионович"]
sex = ["Мужской", "Женский"]
age = [1939, 1941, 1991, 2014, 1917]
weight = [1, 776, 300, 69, 11]
status = ["Новичок", "Опытный", "Эксперт"]