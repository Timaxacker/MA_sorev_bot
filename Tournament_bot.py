#Ass We Can          # Талисман кода



import telebot
from telebot import types
import sqlite3
from sqlite3 import Error
import BDMS
import Key 


bot = telebot.TeleBot(open('API.txt', 'r').read()) # Определенние переменных
connection = BDMS.create_connection("C:\\Users\\79112\\Desktop\\Rep\\MA_sorev_bot\\database.sqlite")
answer = ''
date = Key.date()

information = {}
competitors_db = {}


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

BDMS.execute_query(connection, create_competitors_table)  


@bot.message_handler(commands=["start"]) # Функция по обработке команды /start
def start(m, res=False):
    information[m.from_user.id] = []
    
    bot.send_message(m.chat.id, "Здравствуйте. Напишите, пожалуйста, Ваше ФИО")


@bot.message_handler(content_types=["text"]) # Функция по обработке кнопок
def fio(m):
    global answer

    mess = m.text.strip()
    mas = []
    p = ""

    for ch in mess:
        if ch == " ":
            mas.append(p)
            del(p)
            p = ""
        else: p += ch
    if p != "":
        mas.append(p)
    del(p, mess)

    for d in mas:
        information[m.from_user.id].append(d)
    del(mas)
    

    

    answer = "Напишите, пожалуйста, Ваш год рождения"
    bot.send_message(m.chat.id, answer)
    bot.register_next_step_handler(m, born_year)


def born_year(m):
    global answer

    try:
        information[m.from_user.id].append(int(m.text.strip()))
    except:
        information[m.from_user.id].append(m.text.strip())

    answer = "Напишите, пожалуйста, Ваш вес"
    bot.send_message(m.chat.id, answer)
    bot.register_next_step_handler(m, weight)


def weight(m):
    global answer
    try:
        information[m.from_user.id].append(int(float(m.text.strip())))
    except:
        information[m.from_user.id].append(m.text.strip())

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Новичок")
    markup.add(item1)
    item2=types.KeyboardButton("Опытный")
    markup.add(item2)
    item3=types.KeyboardButton("Эксперт")
    markup.add(item3)

    answer = "Напишите, пожалуйста, Вашу категорию"
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    bot.register_next_step_handler(m, status)


def status(m):
    global answer

    if not(m.text.strip() in ["Новичок", "Опытный", "Эксперт"]):
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, status)

    else:

        information[m.from_user.id].append(m.text.strip())

        competitors_db[m.from_user.id] = date.encrypt(information[m.from_user.id])

        answer = str(information[m.from_user.id])
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, fio)

        print(competitors_db)
        print(information)
        print(date.decrypt(competitors_db[m.from_user.id].copy()))

bot.polling(none_stop=True, interval=0) # Запуск бота



"""
date = Key.date()
a = date.encrypt(["тима", "лазарев", 40, 12])
print(a)
b = date.decrypt(a)
print(b)
"""