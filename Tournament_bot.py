#Ass We Can          # Талисман кода



import telebot
from telebot import types
import exceptionHandler as exch
from random import choice as c, randint as r
from datetime import date, datetime
import traceback
import DBMS
import sys
import Key
import setka
import csv
from math import inf


# print("ë" == "ё")
# print(f"{sys.path[0]}/database.sqlite")
# data = setka.compute_without_gui(f"{sys.path[0]}/database.sqlite")
# with open('categories.csv', 'w') as f:
#     writer = csv.writer(f, delimiter=';')
#     rows = [("Пол", "Пояс", "Возраст", "Вес")]
#     for key, value in data.groups.items():
#         # print(value)
#         age = value['age']
#         weight = value['weight']
#         rows.append(
#             (value['sex'],
#             value['belt'],
#             setka.beautiful_output(setka.ages[age], "a"),  # f"{setka.ages[age][0]}-{setka.ages[age][1]}",
#             setka.beautiful_output(setka.check_weight(setka.weights, setka.ages[age][1], weight, value['sex']), "w"))
#         )
#         for j in value['peoples'].values():
#             d = setka.beautiful_output(j, "p")
#             rows.append(('-', d[0], d[1], d[2]))
#         rows.append(())
#     writer.writerows(rows)


bot = telebot.TeleBot(open('API.txt', 'r').read())
exch.bot = bot
# print(f"{sys.path[0]}database.sqlite")
connection = DBMS.create_connection(f"{sys.path[0]}/database.sqlite")
answer = ''
# date = Key.date()

information = {}
competitors_db = {}


#DBMS.execute_query(connection, DBMS.delete)

# print(1)
# DBMS.execute_query(connection, DBMS.create_competitors_table)

# with open('input.txt', 'w', encoding = 'UTF-8') as f:
#     print('%-14s %-14s %-14s %-14s %-14s %-14s %-14s %-14s' % ("ID", "Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес", "Категория"), file = f)


@exch.exceptioHandlerBot(level=0)
@bot.message_handler(commands=["start"])
def start(m, res=False):
    information[m.from_user.id] = {}
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    lst_of_but = ["Согласен(а)", "Не согласен(а)"]
    answer = "Здравствуйте, это тестовая версия бота, работающая с 15 до 28 января. Просим оставить отзыв о робате в группе - https://t.me/tournament_feedback. Если возникают какие-то ошибки и недочеты, скидывайте, пожалуйста, скриншоты"
    bot.send_message(m.chat.id, answer)
        
    for i in lst_of_but:
        markup.add(types.KeyboardButton(i))

    if m.from_user.id in eval(open('Admins ID.txt', 'r').read()):
        information[m.from_user.id] = {}
        
        answer = "Код:"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, admin_code)

    else:
        answer = 'Для продолжения Вам <u><i><b>ТРЕБУЕТСЯ</b></i></u> согласиться на <a href="https://10.rkn.gov.ru/docs/10/Pravila_obrabotki_PD.pdf">обработку персональных данных</a>'
        bot.send_message(m.chat.id, answer, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(m, pers_data)


@exch.exceptioHandlerBot(level=0)
# @bot.message_handler(content_types=["text"])
def _pers_data(m):
    information[m.from_user.id] = {}

    if m.text.strip() == "Согласен(а)":
        answer = "<u><i><b>НАПИШИТЕ</b></i></u>, пожалуйста, ФИО участника\n(Иванов Иван Иванович)"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, fio)

    elif m.text.strip() == "Не согласен(а)":
        answer = "Для продолжения Вам <u><i><b>ТРЕБУЕТСЯ</b></i></u> согласится на обработку персональных данных"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, pers_data)

    else:
        answer = "<u><i><b>НАЖИМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, pers_data)
    return True


def pers_data(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _pers_data(m):
            bot.register_next_step_handler(m, pers_data)
    else:
        bot.register_next_step_handler(m, pers_data)


@exch.exceptioHandlerBot(level=0)
def _admin_code(m):
    if m.text.strip() == '777':
        answer = "Вы перешли в режим БОГАААААА!!!"

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Файл с участниками", "Файл с категориями"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, admin_menu)
        
    else:
        information[m.from_user.id] = {}
        answer = "Пароль неверный(\nФИО)"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, fio)
    return True


def admin_code(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _admin_code(m):
            bot.register_next_step_handler(m, admin_code)
    else:
        bot.register_next_step_handler(m, admin_code)


@exch.exceptioHandlerBot(level=0)
def _fio(m):
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
        answer = "ФИО введен некорректно! Попытайтесь ещё раз. <u><i><b>ВВОДИТЕ</b></i></u> ФИО в три слова через пробел.\n(Пример: Иванов Иван Иванович)" 
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, fio)

    else:
        information[m.from_user.id]["surname"] = mas[0]
        information[m.from_user.id]["name"] = mas[1]
        information[m.from_user.id]["patronymic"] = mas[2]
        del(mas)
    

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Мужской", "Женский"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))


        answer = "<u><i><b>ВЫБЕРИТЕ</b></i></u>, пожалуйста, пол участника"
        bot.send_message(m.chat.id, answer, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(m, sex)
    return True


def fio(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _fio(m):
            bot.register_next_step_handler(m, fio)
    else:
        bot.register_next_step_handler(m, fio)


#@exch.exceptioHandlerBot(level=0)
#def _phone_number(m):




@exch.exceptioHandlerBot(level=0)
def _sex(m):
    if m.text.strip() in ["Мужской", "Женский"]:
        information[m.from_user.id]["sex"] = m.text.strip()

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(date.today().year-4, date.today().year-105, -1):
            markup.add(types.KeyboardButton(str(i)))

        answer = "<u><i><b>ВЫБЕРИТЕ</b></i></u>, пожалуйста, год рождения участника"
        bot.send_message(m.chat.id, answer, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(m, born_year)

    else:
        answer = "<u><i><b>НАЖИМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, sex)
    return True


def sex(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _sex(m):
            bot.register_next_step_handler(m, sex)
    else:
        bot.register_next_step_handler(m, sex)


@exch.exceptioHandlerBot(level=0)
def _born_year(m):
    for i in range(date.today().year-4, date.today().year-105, -1):
        if m.text.strip() == str(i):
            information[m.from_user.id]["year_born"] = m.text.strip()
            
            answer = "<u><i><b>НАПИШИТЕ</b></i></u>, пожалуйста, вес участника в кг\n(60.0)"
            bot.send_message(m.chat.id, answer, reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")
            bot.register_next_step_handler(m, weight)
            
            break
    
    else:
        answer = "<u><i><b>НАЖИМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, born_year)
    return True


def born_year(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _born_year(m):
            bot.register_next_step_handler(m, born_year)
    else:
        bot.register_next_step_handler(m, born_year)


@exch.exceptioHandlerBot(level=0)
def _weight(m):
    try:
        weight_check = ""
        for lett in m.text.strip():
            if lett in  "0123456789.":
                weight_check += lett
            elif lett == ",":
                weight_check += "."
#             print(lett, weight_check)
        weight_check = float(weight_check)
        if 0 < weight_check < 333:
            information[m.from_user.id]["weight"] = weight_check


            weights_ages = DBMS.execute_read_query(connection, DBMS.select_weights_intervals_age)
            
            for i in weights_ages:
                if int(i[1].split('-')[0]) <= date.today().year - int(information[m.from_user.id]["year_born"]) <= int(i[1].split('-')[1]):
                    DBMS.id_weights = i[0]

            else:
                if date.today().year - int(information[m.from_user.id]["year_born"]) > 50:
                    DBMS.id_weights = 11


            DBMS.weights = DBMS.execute_read_query(connection, DBMS.select_weights_id + str(DBMS.id_weights))
#             print(DBMS.weights)
#             print(information[m.from_user.id]["year_born"])

            if date.today().year - int(information[m.from_user.id]["year_born"]) <= 11:
                print("f")
                for i in DBMS.weights[0]:
#                     print(i)
                    try:
#                         print("p")
                        if weight_check <= float(i):
                            print(i, "c")
                            information[m.from_user.id]["weight_cat"] = str(i)
                            break
                        

                    except ValueError:
#                         print("o")
                        for i in range(len(DBMS.weights[0])-1, 0, -1):
                            if DBMS.weights[0][i] != '':
                                information[m.from_user.id]["weight_cat"] = str(DBMS.weights[0][i])
                                break

                        break    

                else:
                    for i in range(len(DBMS.weights[0])-1, 0, -1):
                        if DBMS.weights[0][i] != '':
                            information[m.from_user.id]["weight_cat"] = str(DBMS.weights[0][i])
                            break

                    

            elif date.today().year - int(information[m.from_user.id]["year_born"]) > 11:
#                 print("f")
                for i in DBMS.weights[0]:
#                     print(i)
                    try:
#                         print(float(i.split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")]))
                        if weight_check <= float(i.split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")]):
#                             print(i, "c")
                            information[m.from_user.id]["weight_cat"] = i.split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")]
                            break
                    

                    except ValueError:
#                         print("i")
                        
                        if i.split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")] == '':
#                             print("98")
                            for i in range(len(DBMS.weights[0])-1, 0, -1):
                                if DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")] != '':
                                    information[m.from_user.id]["weight_cat"] = str(DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")])
                                    break

                        else:
#                             print("y")
                            #for i in range(len(DBMS.weights[0])-1, 0, -1):
#                             print(i.split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")], "u")
                                #if DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")] != '':
                            information[m.from_user.id]["weight_cat"] = i.split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")]
                                    #break

                        break
                        

                else:
#                     print("q")
                    for i in range(len(DBMS.weights[0])-1, 0, -1):
                        if DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")] != '':
                            information[m.from_user.id]["weight_cat"] = str(DBMS.weights[0][i].split("/")[0+int(information[m.from_user.id]["sex"] == "Женский")])
                            break
            
        else:
            b = a[0]


        ages = DBMS.execute_read_query(connection, DBMS.select_ages_intervals)
        lst_of_but = []

        for i in ages:
            if i[0] <= date.today().year - int(information[m.from_user.id]["year_born"]) <= i[1]:
                lst_of_but.append(i[2])

        information[m.from_user.id]["buttons"] = lst_of_but

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        answer = "<u><i><b>ВЫБЕРИТЕ</b></i></u>, пожалуйста, пояс участника"
        bot.send_message(m.chat.id, answer, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(m, belt)
    
    except:
        answer = "Вес введен некорректно! Попытайтесь ещё раз.\n(Пример: 60.0)"
        bot.send_message(m.chat.id, answer)
        bot.register_next_step_handler(m, weight)
    return True


def weight(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _weight(m):
            bot.register_next_step_handler(m, weight)
    else:
        bot.register_next_step_handler(m, weight)


@exch.exceptioHandlerBot(level=0)
def _belt(m):
#     print(information[m.from_user.id])
    if m.text.strip() in information[m.from_user.id]["buttons"]:
        information[m.from_user.id]["belt"] = m.text.strip()

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Strela", "Legion", "Universal Jiu Jitsu", "Sport Generation","Killer Bunny BJJ", "Dragons Den Russia", "Octobus", "Gymnasium", "Другая команда"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))


        answer = "<u><i><b>ВЫБЕРИТЕ</b></i></u>, пожалуйста, команду участника"
        bot.send_message(m.chat.id, answer, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(m, team)
        

    else:
        answer = "<u><i><b>НАЖИМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, belt)
    return True


def belt(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _belt(m):
            bot.register_next_step_handler(m, belt)
    else:
        bot.register_next_step_handler(m, belt)


@exch.exceptioHandlerBot(level=0)   
def _team(m):
    if m.text.strip() in ["Strela", "Legion", "Universal Jiu Jitsu", "Sport Generation","Killer Bunny BJJ", "Dragons Den Russia", "Octobus", "Gymnasium"]:
        information[m.from_user.id]["team"] = m.text.strip()

        answer = "<u><i><b>НАПИШИТЕ</b></i></u>, пожалуйста, фамилию и имя тренера"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, trainer)

    elif m.text.strip() == "Другая команда":
        answer = "<u><i><b>НАПИШИТЕ</b></i></u>, пожалуйста, название команды"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, other_team)

    else:
        answer = "<u><i><b>НАЖИМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, team)
    return True


def team(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _team(m):
            bot.register_next_step_handler(m, team)
    else:
        bot.register_next_step_handler(m, team)


@exch.exceptioHandlerBot(level=0)
def _other_team(m):
    information[m.from_user.id]["team"] = m.text.strip()
    
    answer = "<u><i><b>НАПИШИТЕ</b></i></u>, пожалуйста, фамилию и имя тренера"
    bot.send_message(m.chat.id, answer, parse_mode="HTML")
    bot.register_next_step_handler(m, trainer)
    return True
def other_team(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _other_team(m):
            bot.register_next_step_handler(m, other_team)
    else:
        bot.register_next_step_handler(m, other_team)


@exch.exceptioHandlerBot(level=0)
def _trainer(m):
    information[m.from_user.id]["trainer"] = m.text.strip()

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    lst_of_but = ["Всё корректно", "Не всё корректно"]
    for i in lst_of_but:
        markup.add(types.KeyboardButton(i))

    answer = f"Проверьте достоверность информации\nФамилия: {information[m.from_user.id]['surname']}\nИмя: {information[m.from_user.id]['name']}\nОтчество: {information[m.from_user.id]['patronymic']}\nПол: {information[m.from_user.id]['sex']}\nГод рождения: {information[m.from_user.id]['year_born']}\nВес: {information[m.from_user.id]['weight']}\nПояс: {information[m.from_user.id]['belt']}\nКоманда: {information[m.from_user.id]['team']}\nТренер: {information[m.from_user.id]['trainer']}"
    bot.send_message(m.chat.id, answer, reply_markup=markup)
    bot.register_next_step_handler(m, check)
    return True


def trainer(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _trainer(m):
            bot.register_next_step_handler(m, trainer)
    else:
        bot.register_next_step_handler(m, trainer)


@exch.exceptioHandlerBot(level=0)
def _check(m):
    if m.text.strip() == 'Всё корректно':
        #print(tuple(information[m.from_user.id].values())[:6] + tuple(information[m.from_user.id].values())[8:])
        
        q = 0
        while True:
            
            try:
                
                info = (f'{m.from_user.id}_{q}', ) + tuple(information[m.from_user.id].values())[:6] + tuple(information[m.from_user.id].values())[8:]
                DBMS.add_information_in_competitors(connection, info)
                break

            except:
                q += 1

#         for i in range(300):
#             print(i)
#             info = (r(1, 10e7), c(DBMS.surnames), c(DBMS.names), c(DBMS.patronymics), c(DBMS.sex), c(DBMS.age), c(DBMS.weight), c(DBMS.belt), c(DBMS.teams), c(DBMS.trainers))
#             DBMS.add_information_in_competitors(connection, info)

        if DBMS.error == True:
            answer = "Ой, что-то пошло не так. Пожалуйста, попытайтесь зарегистрироваться ещё раз"
            bot.send_message(m.chat.id, answer)

            answer = "<u><i><b>НАЖМИТЕ</b></i></u> на /start"
            bot.send_message(m.chat.id, answer, parse_mode="HTML")


        else:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            lst_of_but = ["Зарегистрировать еще одного участника"]
            for i in lst_of_but:
                markup.add(types.KeyboardButton(i))
            
            information[m.from_user.id] = {}

            answer = "Вы успешно зарегистрировались"
            bot.send_message(m.chat.id, answer, reply_markup=markup)
            bot.register_next_step_handler(m, new_competitor)
    

    elif m.text.strip() == 'Не всё корректно':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        lst_of_but = ["Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес", "Пояс", "Команда", "Тренер"]
        for i in lst_of_but:
            markup.add(types.KeyboardButton(i))

        answer = "Что именно некорректно?"
        bot.send_message(m.chat.id, answer, reply_markup=markup)
        bot.register_next_step_handler(m, criter)

    
    else:
        answer = "<u><i><b>НАЖМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, check)
    return True


def check(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _check(m):
            bot.register_next_step_handler(m, check)
    else:
        bot.register_next_step_handler(m, check)


@exch.exceptioHandlerBot(level=0)
def _new_competitor(m):
    if m.text.strip() == "Зарегистрировать еще одного участника":
        answer = "<u><i><b>НАПИШИТЕ</b></i></u>, пожалуйста, ФИО участника\n(Иванов Иван Иванович)"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, fio)

    else:
        answer = "<u><i><b>НАЖМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, new_competitor)
    return True


def new_competitor(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _new_competitor(m):
            bot.register_next_step_handler(m, new_competitor)
    else:
        bot.register_next_step_handler(m, new_competitor)


@exch.exceptioHandlerBot(level=0)
def _criter(m):
    global new_value_ind
    new_value_ind = None

    if m.text.strip() in ["Пол", "Год рождения", "Пояс"]:
        if m.text.strip() == 'Год рождения':
            new_value_ind = 4

            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(date.today().year-4, date.today().year-105, -1):
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
                if i[0] <= date.today().year - int(information[m.from_user.id][4]) <= i[1]:
                    lst_of_but.append(i[2])

            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in lst_of_but:
                markup.add(types.KeyboardButton(i))


        answer = "<u><i><b>ВЫБЕРИТЕ</b></i></u> новое значение"
        bot.send_message(m.chat.id, answer, reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(m, new_value)

    else:
        lst = ["Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "", "Вес", "Пояс", "Команда", "Тренер"]
        for i in range(len(lst)):
            if i in [3, 4, 5, 7]: continue

            if m.text.strip() == lst[i]:
                new_value_ind = i
                answer = "<u><i><b>НАПИШИТЕ</b></i></u> новое значение"
                bot.send_message(m.chat.id, answer, parse_mode="HTML")
                bot.register_next_step_handler(m, new_value)
                break

        else:
            answer = "<u><i><b>НАЖИМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
            bot.send_message(m.chat.id, answer, parse_mode="HTML")
            bot.register_next_step_handler(m, criter)
    return True


def criter(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _criter(m):
            bot.register_next_step_handler(m, criter)
    else:
        bot.register_next_step_handler(m, criter)


@exch.exceptioHandlerBot(level=0)
def _new_value(m):
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
                    if int(i[1].split('-')[0]) <= date.today().year - int(information[m.from_user.id][4]) <= int(i[1].split('-')[1]):
                        DBMS.id_weights = i[0]

                else:
                    if date.today().year - int(information[m.from_user.id][4]) > 50:
                        DBMS.id_weights = 11


                DBMS.weights = DBMS.execute_read_query(connection, DBMS.select_weights_id + str(DBMS.id_weights))
                print(DBMS.weights)
                print(information[m.from_user.id][4])

                if date.today().year - int(information[m.from_user.id][4]) <= 11:
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

                        

                elif date.today().year - int(information[m.from_user.id][4]) > 11:
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
            answer = "Вес введен некорректно! Попытайтесь ещё раз.\n(Пример: 60.0)"
            bot.send_message(m.chat.id, answer)

            val_pass = False


    elif new_value_ind == 3:
        if m.text.strip() in ["Мужской", "Женский"]:
            information[m.from_user.id][new_value_ind] = m.text.strip()

            val_pass = True
        
        else:
            answer = "<u><i><b>НАЖИМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
            bot.send_message(m.chat.id, answer, parse_mode="HTML")

            val_pass = False


    elif new_value_ind == 4:
        
        for i in range(date.today().year-4, date.today().year-105, -1):
            if m.text.strip() == str(i):
                information[m.from_user.id][new_value_ind] = int(m.text.strip())
                
                val_pass = True
                break

        else:
            answer = "<u><i><b>НАЖИМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
            bot.send_message(m.chat.id, answer, parse_mode="HTML")

            val_pass = False


    elif new_value_ind == 7:
        ages = DBMS.execute_read_query(connection, DBMS.select_ages_intervals)
        check_lst = []

        for i in ages:
            if i[0] <= date.today().year - int(information[m.from_user.id][4]) <= i[1]:
                check_lst.append(i[2])


        if m.text.strip() in check_lst:
            information[m.from_user.id][new_value_ind] = m.text.strip()

            val_pass = True

        else:
            answer = "<u><i><b>НАЖИМАЙТЕ</b></i></u>, пожалуйста, на кнопки, иначе я Вас не понимаю!"
            bot.send_message(m.chat.id, answer, parse_mode="HTML")
            
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

        answer = "<u><i><b>НАЖМИТЕ</b></i></u> на /start"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")


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
    return True


def new_value(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _new_value(m):
            bot.register_next_step_handler(m, new_value)
    else:
        bot.register_next_step_handler(m, new_value)


@exch.exceptioHandlerBot(level=0)
def _admin_menu(m):
    if m.text.strip() == 'Файл с участниками':
        """
        with open('input.txt', 'w', encoding = 'UTF-8') as f:
            print('%-14s %-14s %-14s %-14s %-14s %-14s %-14s %-14s' % ("ID", "Фамилия", "Имя", "Отчество", "Пол", "Год рождения", "Вес", "Пояс"), file = f)
        
        e_read_query(connection, DBMS.select_competitors)
        
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
        bot.register_next_step_handler(m, admin_menu)
        

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

        data = setka.compute_without_gui(f"{sys.path[0]}/database.sqlite")
        # print(data.groups)


        with open('categories.csv', 'wb') as file:  # , encoding="utf-8"
            file.write("Пол;Пояс;Возраст;Вес\n".encode("windows-1251"))
            for key, value in data.groups.items():
                # print(value)
                age = value['age']
                weight = value['weight']
                file.write(f"{value['sex']};{value['belt']};{setka.beautiful_output(setka.ages[age],'a')};{setka.beautiful_output(setka.check_weight(setka.weights,setka.ages[age][1],weight,value['sex']),'w')}\n".encode("windows-1251"))  # f"{setka.ages[age][0]}-{setka.ages[age][1]}",
                    
                for j in value['peoples'].values():
#                     print(j.surname, j.name, j.last_name)
#                     print(j.fio())
                    d = setka.beautiful_output(j, "p")
                    #print(d)
                    inp = f"-;{d[0]};{d[1]};{d[2]}\n"
#                     print(inp)
                    out = ""
                    for ch in inp:
#                         if inp == "ë":
#                             out += "е"
#                         else:
#                             out += ch
                        try:
                            ch.encode("windows-1251")
                            out += ch
                        except:
                            out += "ё"
                            print(ch)
                    print(out)
                    file.write(out.encode("windows-1251"))
                file.write("\n".encode("windows-1251"))
        with open('categories.csv', 'rb') as f:
            bot.send_document(m.chat.id, f)

        bot.register_next_step_handler(m, admin_menu)
        
        
    else:
        answer = "<u><i><b>НАЖИМАЙ</b></i></u> на кнопки!"
        bot.send_message(m.chat.id, answer, parse_mode="HTML")
        bot.register_next_step_handler(m, admin_menu)
    return True


def admin_menu(m):
    if m.text is not None:
        if m.text.strip() == "/end":
            return
        if not _admin_menu(m):
            bot.register_next_step_handler(m, admin_menu)
    else:
        bot.register_next_step_handler(m, admin_menu)


def send_error(text):
    for id_tg in eval(open('Admins ID.txt', 'r').read()):
        try:
            bot.send_message(id_tg, text)
        except:
            pass


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0, long_polling_timeout=0)
        print("success")
    except Exception as e:
        error = traceback.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        errorText = f"An Error has handled at time: \"{datetime.now()}\":\n+>\"{e.__repr__()}\" at line {error.lineno} in func \"bot.polling\", code:\n->\"\"\"{error.line}\"\"\"\nPlease restart the bot."
        print(errorText)
        send_error(errorText)
