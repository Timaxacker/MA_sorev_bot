import sqlite3
from sqlite3 import Error
import pandas as pd

id_weights = None

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
  weight FLOAT,
  belt TEXT,
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


create_belts_table = """
CREATE TABLE IF NOT EXISTS belts (
  id INTEGER PRIMARY KEY,
  belt TEXT,
  min_age INTEGER,
  max_age INTEGER
);
"""

create_belts = """
INSERT INTO
  belts (id, belt, min_age, max_age)
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


create_weights_table = """
CREATE TABLE IF NOT EXISTS weights (
  id INTEGER PRIMARY KEY,
  age TEXT,
  weight0 TEXT,
  weight1 TEXT,
  weight2 TEXT,
  weight3 TEXT,
  weight4 TEXT,
  weight5 TEXT,
  weight6 TEXT,
  weight7 TEXT,
  weight8 TEXT,
  weight9 TEXT,
  weight10 TEXT
);
"""

create_weights = """
INSERT INTO
  weights (id, age, weight0, weight1, weight2, weight3, weight4, weight5, weight6, weight7, weight8, weight9, weight10)
VALUES
  (0, '4-5', '16', '18', '20', '22', '25', '27.5', '30', '33', '36', '39', '42'),
  (1, '6-7', '18', '20', '22.5', '25', '27.5', '30', '33', '36', '39', '42', '46'),
  (2, '8-9', '20', '22.5', '25', '27.5', '30', '33', '36', '40', '44', '49', ''),
  (3, '10-11', '24', '27', '30', '34', '38', '42', '46', '50', '55', '60', ''),
  (4, '12-13', '30/32', '33/35', '36/38', '40/41', '45/45', '50/49', '55/53', '60/58', '65/63', '70/68', '/73'),
  (5, '14-15', '38/36', '42/39', '46/42', '50/46', '55/50', '60/54', '65/58', '70/63', '75/68', '80/74', '/80'),
  (6, '16-17', '45/40', '50/44', '55/48', '60/52', '65/57', '70/62', '76/68', '83/73', '91/73+', '91+/', ''),
  (7, '18-29', '50/44', '55/48', '65/52', '60/57', '70/62', '76/68', '83/74', '91/80', '98/80+', '98+/', ''),
  (8, '30-35', '55/44', '60/48', '65/52', '70/57', '76/62', '83/68', '90/74', '98/80', '110/87', '110+/87+', ''),
  (9, '36-40', '55/44', '60/48', '65/52', '70/57', '76/62', '83/68', '91/74', '98/80', '110/87', '110+/94', '/94+'),
  (10, '41-45', '55/44', '60/48', '65/52', '70/57', '76/62', '83/68', '91/74', '98/80', '110/87', '110+/94', '/94+'),
  (11, '46-50', '55/44', '60/48', '65/52', '70/57', '76/62', '83/68', '91/74', '98/80', '110/87', '110+/94', '/94+')
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
    belt
FROM
    belts
"""


select_weights_intervals_age = """
SELECT
    id,
    age
FROM
    weights
"""


select_weights_id = """
SELECT 
    weight0,
    weight1,
    weight2,
    weight3,
    weight4,
    weight5,
    weight6,
    weight7,
    weight8,
    weight9,
    weight10
FROM
    weights
WHERE id ==""" 
 
def add_information_in_competitors(connection, info):
    add_information_in_competitors_query = """
    INSERT INTO
        competitors (id, surname, name, patronymic, sex, age, weight, belt, team, trainer)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    
    execute_query_values(connection, add_information_in_competitors_query, info)



def output(connection):
    df = pd.read_sql(select_competitors, connection)
    df.to_excel('competitors.xlsx', index=False)



surnames = ["Хуеглотов", "Лазарев", "Белобородов", "Пидоро", "Ващенко"]
names = ["Валера", "Гоша", "Серёжа", "Виктор", "Олежа"]
patronymics = ["Алексеевич", "Михалыч", "Игнатич", "Буратиныч", "Виcсарионович"]
sex = ["Мужской", "Женский"]
age = [1939, 1941, 1991, 2014, 1917]
weight = [1, 110, 77, 69, 11]
belt = ["Белый", "Серо-белый", "Серый", "Серо-чёрный", "Жёлто-белый", "Жёлтый", "Жёлто-чёрный", "Зелёно-белый", "Зелёный",
    "Зелёно-чёрный", "Синий", "Фиолетовый", "Коричневый", "Чёрный", "Красно-чёрный", "Красно-белый", "Красный"]
teams = ["Strela", "Legion", "Universal Jiu Jitsu", "Sport Generation","Killer Bunny BJJ", "Dragons Den Russia", "Octobus", "Gymnasium"]
trainers = ["Иван Михайлович", "Иван Дмитриевич", "Дмитрий Витальевич"]