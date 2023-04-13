#Ass We Can          # Талисман кода



import telebot
from telebot import types
import DBMS
import Key 


bot = telebot.TeleBot(open('API.txt', 'r').read())
connection = DBMS.create_connection("C:\\Users\\79112\\Desktop\\Rep\\MA_sorev_bot\\database.sqlite")
answer = ''
date = Key.date()

information = {}
competitors_db = {}

delete_comment = "DELETE FROM competitors WHERE id > 0"
DBMS.execute_query(connection, delete_comment)

with open('input.txt', 'w', encoding = 'UTF-8') as f:
    print('%-14s %-14s %-14s %-14s %-14s %-14s %-14s' % ("ID", "Фамилия", "Имя", "Отчество", "Год рождения", "Вес", "Категория"), file = f)

@bot.message_handler(commands=["start"]) 
def start(m, res=False):
    information[m.from_user.id] = []

    #DBMS.add_id_in_competitors(connection, (m.from_user.id, ))

    bot.send_message(m.chat.id, "Здравствуйте. Напишите, пожалуйста, Ваше ФИО")


@bot.message_handler(content_types=["text"]) 
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

        info = (m.from_user.id, ) +  tuple(information[m.from_user.id])
        DBMS.add_information_in_competitors(connection, info)

        print(competitors_db)
        print(information)
        print(date.decrypt(competitors_db[m.from_user.id].copy()))

        select_competitors = "SELECT * from competitors"
        competitors = DBMS.execute_read_query(connection, select_competitors)
        try:
            if information[1835294966][4] == 777:
                with open('input.txt', 'a', encoding = 'UTF-8') as f:
                    for competitor in competitors:
                        for i in range(len(competitor)):
                            print('%-15s' % competitor[i], end='', file = f)
                        print(file = f)
        except: pass



        

bot.polling(none_stop=True, interval=0) 



"""
date = Key.date()
a = date.encrypt(["тима", "лазарев", 40, 12])
print(a)
b = date.decrypt(a)
print(b)
"""