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

#DBMS.execute_query(connection, DBMS.create_statuses)

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
        lst_of_but = ["Вывести бд в файл", "Сгенерировать категории"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)
        
    else:
        information[m.from_user.id] = []
        answer = "Пароль неверный(\nФИО)"
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
        answer = "ФИО введен некорректно! Попытайтесь ещё раз. Вводите ФИО в три слова через пробел.\n(Пример: Иванов Иван Иванович)" 
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, fio)

    else:

        for d in mas:
            information[m.from_user.id].append(d)
        del(mas)
    

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Мужской", "Женский"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))


        answer = "Выберите, пожалуйста, Ваш пол"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, sex)


def sex(m):
    if m.text.strip() in ["Мужской", "Женский"]:
        information[m.from_user.id].append(m.text.strip())

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(d.today().year-4, d.today().year-105, -1):
            markup.add(types.KeyboardButton(str(i)))

        answer = "Выберите, пожалуйста, Ваш год рождения"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, born_year)

    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, sex)


def born_year(m):
    for i in range(d.today().year-4, d.today().year-105, -1):
        if m.text.strip() == str(i):
            information[m.from_user.id].append(m.text.strip())
            break
    
    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, born_year)
    

    answer = "Напишите, пожалуйста, Ваш вес в кг\n(60)"
    bot.send_message(m.chat.id, answer)
    bot.register_next_step_handler(m, weight)
    
    
def weight(m):
    try:
        weight_check = int(float(m.text.strip()))
        if 0 < weight_check < 777:
            information[m.from_user.id].append(weight_check)

        else:
            b = a[0]


        ages = DBMS.execute_read_query(connection, DBMS.select_ages_intervals)
        lst_of_but = []

        for i in ages:
            if i[0] <= d.today().year - int(information[m.from_user.id][4]) <= i[1]:
                lst_of_but.append(i[2])

        information[m.from_user.id].append(lst_of_but)

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        answer = "Выберите, пожалуйста, Ваш пояс"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, status)
    
    except:
        answer = "Вес введен некорректно! Попытайтесь ещё раз.\n(Пример: 60)"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, weight)

    
def status(m):
    if m.text.strip() in information[m.from_user.id][6]:
        information[m.from_user.id].pop(6)

        information[m.from_user.id].append(m.text.strip())

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Всё корректно", "Не всё корректно"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))


        answer = f"Проверьте достоверность информации\nФамилия: {information[m.from_user.id][0]}\nИмя: {information[m.from_user.id][1]}\nОтчество: {information[m.from_user.id][2]}\nПол: {information[m.from_user.id][3]}\nГод рождения: {information[m.from_user.id][4]}\nВес: {information[m.from_user.id][5]}\nПояс: {information[m.from_user.id][6]}"
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
        lst_of_but = ["Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес", "Пояс"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

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

    if m.text.strip() in ["Пол", "Год рождения", "Пояс"]:
        if m.text.strip() == 'Год рождения':
            new_value_ind = 4

            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(d.today().year-4, d.today().year-105, -1):
                markup.add(types.KeyboardButton(str(i)))
        
        elif m.text.strip() == 'Пол':
        
            new_value_ind = 3
        
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            lst_of_but = ["Мужской", "Женский"]
            for i in lst_of_but:
                markup.add(types.KeyboardButton(i))
        
        elif m.text.strip() == 'Пояс':
            new_value_ind = 6
        
            ages = DBMS.execute_read_query(connection, DBMS.select_ages_intervals)
            lst_of_but = []

            for i in ages:
                if i[0] <= d.today().year - int(information[m.from_user.id][4]) <= i[1]:
                    lst_of_but.append(i[2])

            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in lst_of_but:
                markup.add(types.KeyboardButton(i))

        answer = "Выберите новое значение"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, new_value)

    else:
        lst = ["Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес"]
        for i in range(len(lst)):
            if i in [3, 4]: continue

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
    val_pass = None
    
    if new_value_ind in [0, 1, 2]:
        information[m.from_user.id][new_value_ind] = m.text.strip()

        val_pass = True


    elif new_value_ind == 5:
        try:
            weight_check = int(float(m.text.strip()))
            if 0 < weight_check < 777:
                information[m.from_user.id][new_value_ind] = weight_check
                
                val_pass = True

            else:
                b = a[0]


        except:
            answer = "Вес введен некорректно! Попытайтесь ещё раз.\n(Пример: 60)"
            bot.send_message(m.chat.id, answer)

            val_pass = False


    elif new_value_ind == 3:
        if m.text.strip() in ["Мужской", "Женский"]:
            information[m.from_user.id][new_value_ind] = m.text.strip()

            val_pass = True
        
        else:
            answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
            bot.send_message(m.chat.id, answer)

            val_pass = False


    elif new_value_ind == 4:
        
        for i in range(d.today().year-4, d.today().year-105, -1):
            if m.text.strip() == str(i):
                information[m.from_user.id][new_value_ind] = int(m.text.strip())
                
                val_pass = True
                break

        else:
            answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
            bot.send_message(m.chat.id, answer)

            val_pass = False


    elif new_value_ind == 6:
        ages = DBMS.execute_read_query(connection, DBMS.select_ages_intervals)
        check_lst = []

        for i in ages:
            if i[0] <= d.today().year - int(information[m.from_user.id][4]) <= i[1]:
                check_lst.append(i[2])


        if m.text.strip() in check_lst:
            information[m.from_user.id][new_value_ind] = m.text.strip()

            val_pass = True

        else:
            answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
            bot.send_message(m.chat.id, answer)
            
            val_pass = False

    else:
        answer = "Ой, что-то пошло не так. Пожалуйста, попытайтесь зарегистрироваться ещё раз"
        bot.send_message(m.chat.id, answer)

        answer = "Нажмите на /start"
        bot.send_message(m.chat.id, answer)


    if val_pass:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Всё корректно", "Не всё корректно"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        answer = f"Проверьте достоверность информации\nФамилия: {information[m.from_user.id][0]}\nИмя: {information[m.from_user.id][1]}\nОтчество: {information[m.from_user.id][2]}\nПол: {information[m.from_user.id][3]}\nГод рождения: {information[m.from_user.id][4]}\nВес: {information[m.from_user.id][5]}\nПояс: {information[m.from_user.id][6]}"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, check)

    else:
        bot.register_next_step_handler(m, new_value)

    

def admin_menu(m):
    if m.text.strip() == 'Вывести бд в файл':
        with open('input.txt', 'w', encoding = 'UTF-8') as f:
            print('%-14s %-14s %-14s %-14s %-14s %-14s %-14s %-14s' % ("ID", "Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес", "Пояс"), file = f)
        
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

        
        
    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, admin_menu)

        

bot.polling(none_stop=True, interval=0)