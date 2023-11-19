#Ass We Can          # Талисман кода



import telebot
from telebot import types
from random import choice as c, randint as r
from datetime import date as d
import DBMS
import Key 
import pandas as pd
import setka
import csv


bot = telebot.TeleBot(open('API.txt', 'r').read())
connection = DBMS.create_connection("C:\\Users\\79112\\Desktop\\Rep\\MA_sorev_bot\\database.sqlite")
answer = ''
date = Key.date()

information = {}
competitors_db = {}

DBMS.execute_query(connection, DBMS.delete)

#DBMS.execute_query(connection, DBMS.create_competitors_table)

"""
with open('input.txt', 'w', encoding = 'UTF-8') as f:
    print('%-14s %-14s %-14s %-14s %-14s %-14s %-14s %-14s' % ("ID", "Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес", "Категория"), file = f)
"""
    
def beautiful_output(data_cur, tupe):
    out = ""
    if tupe == "p":
        data_cur = data_cur.split(";")
        for i in data_cur:
            out += f"{i} "
    elif tupe in ("a", "w"):
        # data_cur = data_cur.split("-")
        if data_cur[1] == "inf":
            out += f"{data_cur[0]}+"
        else:
            out += f"{data_cur[0]}-{data_cur[1]}"
    return out

@bot.message_handler(commands=["start"]) 
def start(m, res=False):
    information[m.from_user.id] = []
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    lst_of_but = ["Согласен(а)", "Не согласен(а)"]
    for i in lst_of_but:
        markup.add(types.KeyboardButton(i))

    if m.from_user.id in eval(open('Admins ID.txt', 'r').read()):
        answer = "Код:"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, admin_code)

    else:
        answer = 'Здравствуйте. Для продолжения Вам требуется согласиться на <a href="https://10.rkn.gov.ru/docs/10/Pravila_obrabotki_PD.pdf">обработку персональных данных</a>'
        bot.send_message(m.chat.id, answer, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(m, pers_data)


@bot.message_handler(content_types=["text"]) 
def pers_data(m):
    if m.text.strip() == "Согласен(а)":
        answer = "Напишите, пожалуйста, ФИО участника\n(Иванов Иван Иванович)"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, fio)

    elif m.text.strip() == "Не согласен(а)":
        answer = "Для продолжения Вам требуется согласится на обработку персональных данных"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, pers_data)

    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, pers_data)

def admin_code(m):
    if m.text.strip() == '777':
        answer = "Вы перешли в режим БОГАААААА!!!"

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Файл с участниками", "Файл с категориями"]
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


        answer = "Выберите, пожалуйста, пол участника"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, sex)


def sex(m):
    if m.text.strip() in ["Мужской", "Женский"]:
        information[m.from_user.id].append(m.text.strip())

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(d.today().year-4, d.today().year-105, -1):
            markup.add(types.KeyboardButton(str(i)))

        answer = "Выберите, пожалуйста, год рождения участника"
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
            
            answer = "Напишите, пожалуйста, вес участника в кг\n(60)"
            bot.send_message(m.chat.id, answer)
            bot.register_next_step_handler(m, weight)
            
            break
    
    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, born_year)
    

    
def weight(m):
    try:
        weight_check = ""
        for lett in m.text.strip():
            if lett in  "0123456789.":
                weight_check += lett
            elif lett == ",":
                weight_check += "."
            print(lett, weight_check)
        weight_check = float(weight_check)
        if 0 < weight_check < 333:
            information[m.from_user.id].append(weight_check)


            weights_ages = DBMS.execute_read_query(connection, DBMS.select_weights_intervals_age)
            
            for i in weights_ages:
                if int(i[1].split('-')[0]) <= d.today().year - int(information[m.from_user.id][4]) <= int(i[1].split('-')[1]):
                    DBMS.id_weights = i[0]

            else:
                if d.today().year - int(information[m.from_user.id][4]) > 50:
                    DBMS.id_weights = 11


            DBMS.weights = DBMS.execute_read_query(connection, DBMS.select_weights_id + str(DBMS.id_weights))
            print(DBMS.weights)
            print(information[m.from_user.id][4])

            if d.today().year - int(information[m.from_user.id][4]) <= 11:
                print("f")
                for i in DBMS.weights[0]:
                    print(i)
                    try:
                        print("p")
                        if weight_check <= float(i):
                            print(i, "c")
                            information[m.from_user.id].append(str(i))
                            break
                        

                    except ValueError:
                        print("o")
                        for i in range(len(DBMS.weights[0])-1, 0, -1):
                            if DBMS.weights[0][i] != '':
                                information[m.from_user.id].append(str(DBMS.weights[0][i]))
                                break

                        break    

                else:
                    for i in range(len(DBMS.weights[0])-1, 0, -1):
                        if DBMS.weights[0][i] != '':
                            information[m.from_user.id].append(str(DBMS.weights[0][i]))
                            break

                    

            elif d.today().year - int(information[m.from_user.id][4]) > 11:
                print("f")
                for i in DBMS.weights[0]:
                    print(i)
                    try:
                        print(float(i.split("/")[0+int(information[m.from_user.id][3] == "Женский")]))
                        if weight_check <= float(i.split("/")[0+int(information[m.from_user.id][3] == "Женский")]):
                            print(i, "c")
                            information[m.from_user.id].append(i.split("/")[0+int(information[m.from_user.id][3] == "Женский")])
                            break
                    

                    except ValueError:
                        print("i")
                        
                        if i.split("/")[0+int(information[m.from_user.id][3] == "Женский")] == '':
                            print("98")
                            for i in range(len(DBMS.weights[0])-1, 0, -1):
                                if DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id][3] == "Женский")] != '':
                                    information[m.from_user.id].append(str(DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id][3] == "Женский")]))
                                    break

                        else:
                            print("y")
                            #for i in range(len(DBMS.weights[0])-1, 0, -1):
                            print(i.split("/")[0+int(information[m.from_user.id][3] == "Женский")], "u")
                                #if DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id][3] == "Женский")] != '':
                            information[m.from_user.id].append(i.split("/")[0+int(information[m.from_user.id][3] == "Женский")])
                                    #break

                        break
                        

                else:
                    print("q")
                    for i in range(len(DBMS.weights[0])-1, 0, -1):
                        if DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id][3] == "Женский")] != '':
                            information[m.from_user.id].append(str(DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id][3] == "Женский")]))
                            break
            
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

        answer = "Выберите, пожалуйста, пояс участника"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, belt)
    
    except:
        answer = "Вес введен некорректно! Попытайтесь ещё раз.\n(Пример: 60)"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, weight)


def belt(m):
    print(information[m.from_user.id])
    if m.text.strip() in information[m.from_user.id][7]:
        information[m.from_user.id].pop(7)

        information[m.from_user.id].append(m.text.strip())

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Strela", "Legion", "Universal Jiu Jitsu", "Sport Generation","Killer Bunny BJJ", "Dragons Den Russia", "Octobus", "Gymnasium", "Другая команда"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))


        answer = "Выберите, пожалуйста, команду участника"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, team)
        

    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, belt)
        
def team(m):
    if m.text.strip() in ["Strela", "Legion", "Universal Jiu Jitsu", "Sport Generation","Killer Bunny BJJ", "Dragons Den Russia", "Octobus", "Gymnasium"]:
        information[m.from_user.id].append(m.text.strip())

        answer = "Напишите, пожалуйста, фамилию и имя тренера участника"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, trainer)

    elif m.text.strip() == "Другая команда":
        answer = "Напишите, пожалуйста, название команды участника"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, other_team)

    else:
        answer = "Нажимайте, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, team)

    
def other_team(m):
    information[m.from_user.id].append(m.text.strip())
    
    answer = "Напишите, пожалуйста, фамилию и имя тренера участника"
    bot.send_message(m.chat.id, answer)
    bot.register_next_step_handler(m, trainer)



def trainer(m):
    information[m.from_user.id].append(m.text.strip())

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    lst_of_but = ["Всё корректно", "Не всё корректно"]
    for i in lst_of_but:
        markup.add(types.KeyboardButton(i))

    answer = f"Проверьте достоверность информации\nФамилия: {information[m.from_user.id][0]}\nИмя: {information[m.from_user.id][1]}\nОтчество: {information[m.from_user.id][2]}\nПол: {information[m.from_user.id][3]}\nГод рождения: {information[m.from_user.id][4]}\nВес: {information[m.from_user.id][5]}\nПояс: {information[m.from_user.id][7]}\nКоманда: {information[m.from_user.id][8]}\nТренер: {information[m.from_user.id][9]}"
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    bot.register_next_step_handler(m, check)


def check(m):
    if m.text.strip() == 'Всё корректно':
        info = (m.from_user.id, ) +  tuple(information[m.from_user.id][:5]) + tuple(information[m.from_user.id][6:])
        DBMS.add_information_in_competitors(connection, info)

        for i in range(300):
            info = (r(1, 10e7), c(DBMS.surnames), c(DBMS.names), c(DBMS.patronymics), c(DBMS.sex), c(DBMS.age), c(DBMS.weight), c(DBMS.belt), c(DBMS.teams), c(DBMS.trainers))
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
        lst_of_but = ["Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес", "Пояс", "Команда", "Тренер"]
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
            new_value_ind = 7
        
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
        lst = ["Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "", "Вес", "Пояс", "Команда", "Тренер"]
        for i in range(len(lst)):
            if i in [3, 4, 5, 7]: continue

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


    elif new_value_ind == 6:
        try:
            weight_check = ""
            for lett in m.text.strip():
                if lett in  "0123456789.":
                    weight_check += lett
                elif lett == ",":
                    weight_check += "."
                print(lett, weight_check)
            weight_check = float(weight_check)
            if 0 < weight_check < 777:
                information[m.from_user.id][new_value_ind-1] = weight_check


                weights_ages = DBMS.execute_read_query(connection, DBMS.select_weights_intervals_age)
            
                for i in weights_ages:
                    if int(i[1].split('-')[0]) <= d.today().year - int(information[m.from_user.id][4]) <= int(i[1].split('-')[1]):
                        DBMS.id_weights = i[0]

                else:
                    if d.today().year - int(information[m.from_user.id][4]) > 50:
                        DBMS.id_weights = 11


                DBMS.weights = DBMS.execute_read_query(connection, DBMS.select_weights_id + str(DBMS.id_weights))
                print(DBMS.weights)
                print(information[m.from_user.id][4])

                if d.today().year - int(information[m.from_user.id][4]) <= 11:
                    print("f")
                    for i in DBMS.weights[0]:
                        print(i)
                        try:
                            print("p")
                            if weight_check <= float(i):
                                print(i, "c")
                                information[m.from_user.id][new_value_ind] = str(i)
                                break
                            

                        except ValueError:
                            print("o")
                            for i in range(len(DBMS.weights[0])-1, 0, -1):
                                if DBMS.weights[0][i] != '':
                                    information[m.from_user.id][new_value_ind] = str(DBMS.weights[0][i])
                                    break

                            break    

                    else:
                        for i in range(len(DBMS.weights[0])-1, 0, -1):
                            if DBMS.weights[0][i] != '':
                                information[m.from_user.id][new_value_ind] = str(DBMS.weights[0][i])
                                break

                        

                elif d.today().year - int(information[m.from_user.id][4]) > 11:
                    print("f")
                    for i in DBMS.weights[0]:
                        print(i)
                        try:
                            print(float(i.split("/")[0+int(information[m.from_user.id][3] == "Женский")]))
                            if weight_check <= float(i.split("/")[0+int(information[m.from_user.id][3] == "Женский")]):
                                print(i, "c")
                                information[m.from_user.id][new_value_ind] = i.split("/")[0+int(information[m.from_user.id][3] == "Женский")]
                                break
                        

                        except ValueError:
                            print("i")
                            
                            if i.split("/")[0+int(information[m.from_user.id][3] == "Женский")] == '':
                                print("98")
                                for i in range(len(DBMS.weights[0])-1, 0, -1):
                                    if DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id][3] == "Женский")] != '':
                                        information[m.from_user.id][new_value_ind] = str(DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id][3] == "Женский")])
                                        break

                            else:
                                print("y")
                                #for i in range(len(DBMS.weights[0])-1, 0, -1):
                                print(i.split("/")[0+int(information[m.from_user.id][3] == "Женский")], "u")
                                    #if DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id][3] == "Женский")] != '':
                                information[m.from_user.id][new_value_ind] = i.split("/")[0+int(information[m.from_user.id][3] == "Женский")]
                                        #break

                            break
                            

                    else:
                        print("q")
                        for i in range(len(DBMS.weights[0])-1, 0, -1):
                            if DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id][3] == "Женский")] != '':
                                information[m.from_user.id][new_value_ind] = str(DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id][3] == "Женский")])
                                break
            
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


    elif new_value_ind == 7:
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

    elif new_value_ind == 8:
        information[m.from_user.id][new_value_ind] = m.text.strip()

        val_pass = True

    elif new_value_ind == 9:
        information[m.from_user.id][new_value_ind] = m.text.strip()

        val_pass = True


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

        answer = f"Проверьте достоверность информации\nФамилия: {information[m.from_user.id][0]}\nИмя: {information[m.from_user.id][1]}\nОтчество: {information[m.from_user.id][2]}\nПол: {information[m.from_user.id][3]}\nГод рождения: {information[m.from_user.id][4]}\nВес: {information[m.from_user.id][5]}\nПояс: {information[m.from_user.id][7]}\nКоманда: {information[m.from_user.id][8]}\nТренер: {information[m.from_user.id][9]}"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, check)

    else:
        bot.register_next_step_handler(m, new_value)

    

def admin_menu(m):
    if m.text.strip() == 'Файл с участниками':
        """
        with open('input.txt', 'w', encoding = 'UTF-8') as f:
            print('%-14s %-14s %-14s %-14s %-14s %-14s %-14s %-14s' % ("ID", "Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес", "Пояс"), file = f)
        
        competitors = DBMS.execute_read_query(connection, DBMS.select_competitors)
        
        try:
            with open('input.txt', 'a', encoding = 'UTF-8') as f:
                for competitor in competitors:
                    for i in range(len(competitor)):
                        print('%-15s' % competitor[i], end='', file = f)
                    print(file = f)

            #with open('input.txt', 'rb') as f: bot.send_document(m.chat.id, f)

        except:
            print("Error")
    """

        DBMS.output(connection)
        with open('competitors.xlsx', 'rb') as f:
            bot.send_document(m.chat.id, f)


    elif  m.text.strip() == 'Файл с категориями':
        """
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
        """

        data = setka.compute_without_gui("C:\\Users\\79112\\Desktop\\Rep\\MA_sorev_bot\\database.sqlite")
        # print(data.groups)


        with open('categories.csv', 'w') as f:
            writer = csv.writer(f, delimiter=';')
            for key, value in data.groups.items():
                print(value)
                age = value['age']
                weight = value['weight']
                writer.writerow((value['sex'],
                value['belt'],
                beautiful_output(setka.ages[age], "a"),  # f"{setka.ages[age][0]}-{setka.ages[age][1]}",
                beautiful_output(setka.check_weight(setka.weights, setka.ages[age][1], weight, value['sex']), "w")))  # f"{setka.check_weight(setka.weights, setka.ages[age][1], weight, value['sex'])[0]}-{setka.check_weight(setka.weights, setka.ages[age][1], weight, value['sex'])[1]}"
                for j in value['peoples'].keys():
                    writer.writerow(('', beautiful_output(j, "p")))

        with open('categories.csv', 'rb') as f:
            bot.send_document(m.chat.id, f)
            
        
        
    else:
        answer = "Нажимай на кнопки!"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, admin_menu)

        

bot.polling(none_stop=True, interval=0)