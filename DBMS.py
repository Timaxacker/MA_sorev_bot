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
  status TEXT,
  team TEXT,
  trainer
);
"""


create_ages_table = """
CREATE TABLE IF NOT EXISTS ages (
  id INTEGER PRIMARY KEY
);
"""

create_ages_intervals = """
INSERT INTO
  ages (id, interval)
VALUES
  (0, '4'),
  (1, '5'),
  (2, '6'),
  (3, '7'),
  (4, '8'),
  (5, '9'),
  (6, '10'),
  (7, '11'),
  (8, '12'),
  (9, '13'),
  (10, '14'),
  (11, '15'),
  (12, '16'),
  (13, '17'),
  (14, '18'),
  (15, '19-49'),
  (16, '50-56'),
  (17, '57-66'),
  (18, '67+');
"""


create_statuses_table = """
CREATE TABLE IF NOT EXISTS statuses (
  id INTEGER PRIMARY KEY,
  status TEXT,
  min_age INTEGER,
  max_age INTEGER
);
"""

create_statuses = """
INSERT INTO
  statuses (id, status, min_age, max_age)
VALUES
  (0, 'Белый', 4, 104),
  (1, 'Серый-Белый', 4, 15),
  (2, 'Серый', 4, 15),
  (3, 'Серый-Чёрный', 4, 15),
  (4, 'Жёлтый-Белый', 7, 15),
  (5, 'Жёлтый', 7, 15),
  (6, 'Жёлтый-Чёрный', 7, 15),
  (7, 'Оранжевый-Белый', 10, 15),
  (8, 'Оранжевый', 10, 15),
  (9, 'Оранжевый-Чёрный', 10, 15),
  (10, 'Зелёный-Белый', 13, 15),
  (11, 'Зелёный', 13, 15),
  (12, 'Зелёный-Чёрный', 13, 15),
  (13, 'Синий', 16, 104),
  (14, 'Фиолетовый', 16, 104),
  (15, 'Коричневый', 18, 104),
  (16, 'Чёрный', 19, 104),
  (17, 'Красный-Чёрный', 50, 104),
  (18, 'Красный-Белый', 57, 104),
  (19, 'Красный', 67, 104)
"""


delete = "DELETE FROM competitors WHERE id >= 0"


select_competitors = "SELECT * from competitors"


select_competitors_in_categories = """
SELECT
    id,
    sex,
    age,
    weight,
    status
FROM
    competitors
"""


select_ages_intervals = """
SELECT
    min_age,
    max_age,
    status
FROM
    statuses
"""



def add_information_in_competitors(connection, info):
    add_information_in_competitors_query = """
    INSERT INTO
        competitors (id, surname, name, patronymic, sex, age, weight, status, team, trainer)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    
    execute_query_values(connection, add_information_in_competitors_query, info)





surnames = ["Хуеглотов", "Лазарев", "Белобородов", "Пидоро", "Ващенко"]
names = ["Валера", "Гоша", "Серёжа", "Виктор", "Олежа"]
patronymics = ["Алексеевич", "Михалыч", "Игнатич", "Буратиныч", "Виcсарионович"]
sex = ["Мужской", "Женский"]
age = [1939, 1941, 1991, 2014, 1917]
weight = [1, 776, 300, 69, 11]
status = ["Новичок", "Опытный", "Эксперт"]
teams = ["Strela", "Legion", "Universal Jiu Jitsu", "Sport Generation","Killer Bunny BJJ", "Dragons Den Russia", "Octobus", "Gymnasium"]
trainers = ["Иван Михайлович", "Иван Дмитриевич", "Дмитрий Витальевич"]