#Ass We Can          # Талисман кода



import telebot
from telebot import types
import Key 


bot = telebot.TeleBot('6262757409:AAHsjhCslfRa6kV1q-sZsE4gFgLPrfEAgME') # Определенние переменных
answer = ''

information = {}


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

        answer = str(information[m.from_user.id])
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, fio)

bot.polling(none_stop=True, interval=0) # Запуск бота


"""
date = Key.date()
a = date.encrypt(["тима", "лазарев", 40, 12])
print(a)
b = date.decrypt(a)
print(b)
"""