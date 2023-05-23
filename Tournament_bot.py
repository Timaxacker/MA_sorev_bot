#Ass We Can          # Талисман кода



import telebot
from telebot import types
from random import choice as c, randint as r

from datetime import date as d
import DBMS
import Key 



bot = telebot.TeleBot(open('API.txt', 'r').read())
connection = DBMS.create_connection("C:\\Users\\79112\\Desktop\\Rep\\MA_sorev_bot\\database.sqlite")
answer = ''
date = Key.date()

information = {}
competitors_db = {}

DBMS.execute_query(connection, DBMS.delete)

#DBMS.execute_query(connection, DBMS.delete)
#DBMS.execute_query(connection, DBMS.create_statuses_intervals)

with open('input.txt', 'w', encoding = 'UTF-8') as f:
    print('%-14s %-14s %-14s %-14s %-14s %-14s %-14s %-14s' % ("ID", "Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес", "Категория"), file = f)

@bot.message_handler(commands=["start"]) 
def start(m, res=False):
    if m.from_user.id == int(open('Admins ID.txt', 'r').read()):
        answer = "Код:"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, admin_code)

    else:
        information[m.from_user.id] = []
        answer = "Здравствуйте. Напишите, пожалуйста, Ваше ФИО\n(Иванов Иван Иванович)"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, fio)


@bot.message_handler(content_types=["text"]) 
def admin_code(m):
    if m.text.strip() == '777':
        answer = "Вы перешли в режим БОГАААААА!!!"

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Вывести бд в файл")
        markup.add(item1)
        item2=types.KeyboardButton("Сгенерировать категории")
        markup.add(item2)

        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)
        
    else:
        information[m.from_user.id] = []
        answer = "Пароль неверный(\nФИО"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, fio)


def fio(m):
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

    if len(mas) != 3:
        answer = "ФИО введен некорректно! Попытайтесь еще раз. Вводите ФИО в три слова через пробел.\n(Пример: Иванов Иван Иванович)" 
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, fio)

    else:

        for d in mas:
            information[m.from_user.id].append(d)
        del(mas)
    

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Мужской")
        markup.add(item1)
        item2=types.KeyboardButton("Женский")
        markup.add(item2)

        answer = "Выберите, пожалуйста, Ваш пол"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, sex)

def sex(m):
    if m.text.strip() in ["Мужской", "Женский"]:
        information[m.from_user.id].append(m.text.strip())

        answer = "Напишите, пожалуйста, Ваш год рождения\n(2007)"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, born_year)

    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, sex)

def born_year(m):
    try:
        year_check = int(m.text.strip())
        if 1900 < year_check <= d.today().year:
            information[m.from_user.id].append(year_check)
        
        else:
            b = a[0]
        
        answer = "Напишите, пожалуйста, Ваш вес в кг\n(60)"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, weight)
    
    except:
        answer = "Год рождения введен некорректно! Попытайтесь еще раз.\n(Пример: 2007)"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, born_year)


def weight(m):
    try:
        weight_check = int(float(m.text.strip()))
        if 0 < weight_check < 777:
            information[m.from_user.id].append(weight_check)

        else:
            b = a[0]

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Новичок")
        markup.add(item1)
        item2=types.KeyboardButton("Опытный")
        markup.add(item2)
        item3=types.KeyboardButton("Эксперт")
        markup.add(item3)

        answer = "Выберите, пожалуйста, Вашу категорию"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, status)
    
    except:
        answer = "Вес введен некорректно! Попытайтесь еще раз.\n(Пример: 60)"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, weight)

    
def status(m):
    if m.text.strip() in ["Новичок", "Опытный", "Эксперт"]:
        information[m.from_user.id].append(m.text.strip())

        competitors_db[m.from_user.id] = date.encrypt(information[m.from_user.id])

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Всё корректно")
        markup.add(item1)
        item2=types.KeyboardButton("Не всё корректно")
        markup.add(item2)

        answer = f"Проверьте достоверность информации\nФамилия: {information[m.from_user.id][0]}\nИмя: {information[m.from_user.id][1]}\nОтчество: {information[m.from_user.id][2]}\nПол: {information[m.from_user.id][3]}\nГод рождения: {information[m.from_user.id][4]}\nВес: {information[m.from_user.id][5]}\nКатегория: {information[m.from_user.id][6]}"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, check)
        

    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, status)
        
  
     
def check(m):
    if m.text.strip() == 'Всё корректно':
        info = (m.from_user.id, ) +  tuple(information[m.from_user.id])
        DBMS.add_information_in_competitors(connection, info)

        for i in range(3):
            info = (r(1, 10e7), c(DBMS.surnames), c(DBMS.names), c(DBMS.patronymics), c(DBMS.sex), c(DBMS.age), c(DBMS.weight), c(DBMS.status))
            DBMS.add_information_in_competitors(connection, info)
        #print(DBMS.error)

        if DBMS.error == True:
            answer = "Ой, что-то пошло не так. Пожалуйста, попытайтесь зарегистрироваться ещё раз"
            bot.send_message(m.chat.id, answer)

            answer = "Нажмите на /start"
            bot.send_message(m.chat.id, answer)
            


        else:
            information[m.from_user.id] = []

            answer = "Вы успешно зарегестрировались"
            bot.send_message(m.chat.id, answer)
    

    elif m.text.strip() == 'Не всё корректно':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Фамилия")
        markup.add(item1)
        item2=types.KeyboardButton("Имя")
        markup.add(item2)
        item3=types.KeyboardButton("Отчество")
        markup.add(item3)
        item4=types.KeyboardButton("Пол")
        markup.add(item4)
        item5=types.KeyboardButton("Год рождения")
        markup.add(item5)
        item6=types.KeyboardButton("Вес")
        markup.add(item6)
        item7=types.KeyboardButton("Категория")
        markup.add(item7)

        answer = "Что именно некорректно?"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, criter)

    
    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, check)


def criter(m):
    global new_value_ind
    new_value_ind = None

    if m.text.strip() in ["Пол", "Категория"]:
        if m.text.strip() == 'Пол':
        
            new_value_ind = 3
        
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Мужской")
            markup.add(item1)
            item2=types.KeyboardButton("Женский")
            markup.add(item2)
        
        elif m.text.strip() == 'Категория':
            new_value_ind = 6
        
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Новичок")
            markup.add(item1)
            item2=types.KeyboardButton("Опытный")
            markup.add(item2)
            item3=types.KeyboardButton("Эксперт")
            markup.add(item3)

        answer = "Выберите новое значение"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, new_value)

    else:
        lst = ["Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес"]
        for i in range(len(lst)):
            if i == 3: continue

            if m.text.strip() == lst[i]:
                new_value_ind = i
                answer = "Напишите новое значение"
                bot.send_message(m.chat.id, answer)
                bot.register_next_step_handler(m, new_value)
                break

        else:
            answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
            bot.send_message(m.chat.id, answer)
            bot.register_next_step_handler(m, criter)
        

def new_value(m):
    if new_value_ind in [0, 1, 2]:
        information[m.from_user.id][new_value_ind] = m.text.strip()

    elif new_value_ind == 4:
        try:
            information[m.from_user.id][new_value_ind] = int(m.text.strip())
        
        except:
            answer = "Год рождения введен некорректно! Попытайтесь еще раз.\n(Пример: 2007)"
            bot.send_message(m.chat.id, answer)
            bot.register_next_step_handler(m, new_value)

    elif new_value_ind == 5:
        try:
            information[m.from_user.id][new_value_ind] = int(float(m.text.strip()))
        
        except:
            answer = "Вес введен некорректно! Попытайтесь еще раз.\n(Пример: 60)"
            bot.send_message(m.chat.id, answer)
            bot.register_next_step_handler(m, new_value)

    elif new_value_ind == 3:
        if m.text.strip() in ["Мужской", "Женский"]:
            information[m.from_user.id][new_value_ind] = m.text.strip()
        
        else:
            answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
            bot.send_message(m.chat.id, answer)
            bot.register_next_step_handler(m, new_value)

    elif new_value_ind == 6:
        if m.text.strip() in ["Новичок", "Опытный", "Эксперт"]:
            information[m.from_user.id][new_value_ind] = m.text.strip()

        else:
            answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
            bot.send_message(m.chat.id, answer)
            bot.register_next_step_handler(m, new_value)

    else:
        answer = "Ой, что-то пошло не так. Пожалуйста, попытайтесь зарегистрироваться ещё раз"
        bot.send_message(m.chat.id, answer)

        answer = "Нажмите на /start"
        bot.send_message(m.chat.id, answer)


    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Всё корректно")
    markup.add(item1)
    item2=types.KeyboardButton("Не всё корректно")
    markup.add(item2)

    answer = f"Проверьте достоверность информации\nФамилия: {information[m.from_user.id][0]}\nИмя: {information[m.from_user.id][1]}\nОтчество: {information[m.from_user.id][2]}\nПол: {information[m.from_user.id][3]}\nГод рождения: {information[m.from_user.id][4]}\nВес: {information[m.from_user.id][5]}\nКатегория: {information[m.from_user.id][6]}"
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    bot.register_next_step_handler(m, check)



def admin_menu(m):
    if m.text.strip() == 'Вывести бд в файл':
        with open('input.txt', 'w', encoding = 'UTF-8') as f:
            print('%-14s %-14s %-14s %-14s %-14s %-14s %-14s %-14s' % ("ID", "Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес", "Категория"), file = f)
        
        competitors = DBMS.execute_read_query(connection, DBMS.select_competitors)
        
        try:
            with open('input.txt', 'a', encoding = 'UTF-8') as f:
                for competitor in competitors:
                    for i in range(len(competitor)):
                        print('%-15s' % competitor[i], end='', file = f)
                    print(file = f)

            with open('input.txt', 'rb') as f: bot.send_document(m.chat.id, f)

        except: print("Error")

    elif  m.text.strip() == 'Сгенерировать категории':
        cat = {}
        
        competitors = DBMS.execute_read_query(connection, DBMS.select_competitors_in_categories)

        for competitor in competitors:
            crit = [0 ,'Мужской', 1991, 300, 'Эксперт']
            
            for i in range(1, 5):
                print(competitor[i], crit[i])

                if competitor[i] != crit[i]:
                    break
            
            else:
                cat[competitor[0]] = []

        print(cat)

        intervals = DBMS.execute_read_query(connection, DBMS.select_ages_intervals)

        for interval in intervals:
            print(interval, type(interval))
        
    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, admin_menu)

        

bot.polling(none_stop=True, interval=0) 



"""
date = Key.date()
a = date.encrypt(["тима", "лазарев", 40, 12])
print(a)
b = date.decrypt(a)
print(b)
"""