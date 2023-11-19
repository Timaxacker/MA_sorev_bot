import tkinter
from tkinter import ttk, messagebox as mb
from tkinter.constants import *
from tkinter import filedialog
from random import randint, choice
from math import inf
import DBMS


belts = [
    "Белый", "Серо-белый", "Серый", "Серо-чёрный", "Жёлто-белый", "Жёлтый", "Жёлто-чёрный", "Зелёно-белый", "Зелёный",
    "Зелёно-чёрный", "Синий", "Фиолетовый", "Коричневый", "Чёрный", "Красно-чёрный", "Красно-белый", "Красный"
]
windows = {"main": tkinter.Tk(className="Сетка V1-5 beta")}
font = ("Arial", 12)
peoples = {}
weights = {
    "[4, 5]-all": {
        "1": [0, 16], "2": [16, 18], "3": [18, 20], "4": [20, 22], "5": [22, 25], "6": [25, 27.5],
        "7": [27.5, 30], "8": [30, 33], "9": [33, 36], "10": [36, 39], "11": [39, 42], "12": [42, inf]
    },
    "[5, 7]-all": {
        "1": [0, 18], "2": [18, 20], "3": [20, 22.5], "4": [22.5, 25], "5": [25, 27.5], "6": [27.5, 30],
        "7": [30, 33], "8": [33, 36], "9": [36, 39], "10": [39, 42], "11": [42, 46], "12": [46, inf]
    },
    "[7, 9]-all": {
        "1": [0, 20], "2": [20, 22.5], "3": [22.5, 25], "4": [25, 27.5], "5": [27.5, 30], "6": [30, 33],
        "7": [33, 36], "8": [36, 40], "9": [40, 44], "10": [44, 49], "11": [49, inf]
    },
    "[9, 11]-all": {
        "1": [0, 24], "2": [24, 27], "3": [27, 30], "4": [30, 34], "5": [34, 38], "6": [38, 42],
        "7": [42, 46], "8": [46, 50], "9": [50, 55], "10": [55, 60], "11": [60, inf]
    },
    "[18, inf]-all": {
        "1": [0, 57.38], "2": [57.38, 69.96], "3": [69.96, 75.98], "4": [75.98, 82.1], "5": [82.1, 88.2],
        "6": [88.2, 94.12], "7": [94.12, 100.24], "8": [100.24, inf]
   }
}
ages = {"June1": [4, 5], "June2": [6, 7], "June3": [8, 9], "June4": [10, 11], "Teen1": [12, 13], "Teen2": [14, 15], "Teen3": [16, 17], "Master0": [18, 29], "Master1": [30, 35], "Master2": [36, 40], "Master3": [41, 45], "Master4": [46, 50], "Master5": [51, inf]}
translate_sex = {"male": "мужской", "female": "женский", "?": "?"}
translate_sex_reverse = {"Мужской": "male", "Женский": "female", "?": "?"}
base_names = ["Иван", "Алесей", "Тимофей", "Дмитрий", "Максим", "Александр", "Сергей", "Илья"]
base_surnames = ["Петров", "Иванов", "Попов", "Васюков", "Минаев", "Лазорев", "Рыбаков", "Белобров"]
base_last_names = ["Михайлович", "Дмитриевич", "Максимович", "Ильич", "Анатольевич", "Дьяченко"]


def is_int(val):
    try:
        float(val)
        return True
    except:
        return False


# def list_from_dict(a: dict)


def check_weight(_weights, _age, _weight_name, _sex):
    for _ages, weights_ in _weights.items():
        _ages = _ages.split("-")
        if _ages[1] != "all":
            if _ages[1] != _sex:
                continue
        _ages[0] = eval(_ages[0])
        if _age > _ages[0][1]:
            continue
        for weight_name, weight_vals in weights_.items():
            if weight_name == _weight_name:
                return weight_vals


def name_weight(_weights, _age, _weight):
    for _ages, weights_ in _weights.items():
        _ages = _ages.split("-")
        if _ages[1] != "all":
            if _ages[1] != _sex:
                continue
        _ages[0] = eval(_ages[0])
        # print(_ages, _age)
        if _age > _ages[0][1]:
            continue
        # print(weights_)
        for weight_name, weight_vals in weights_.items():
            # print(weight_vals, _weight)
            if weight_vals[0] <= _weight <= weight_vals[1]:
                # print(weight_name)
                return weight_name
    # print(111111111111111111111111111111111111111111111111)


def name_age(_ages, _age):
    for age_name, age_vals in _ages.items():
        # print(age_vals)
        if age_vals[0] <= _age <= age_vals[1]:
            return age_name


class People:
    def __init__(self, surname, name, last_name, sex, age, weight, belt, state=False, id_tg=-1):
        self.surname = surname
        self.name = name
        self.last_name = last_name
        self.age = age
        self.belt = belt
        self.weight = weight
        self.sex = sex
        self.state = state
        self.tg_id = id_tg


class Place:
    def __init__(self, f: dict, max_n=7):
        self.pos = {"Мужской": {}, "Женский": {}}
        for i in f.values():
            if not i.state:
                continue
            # i.sex = translate_sex_reverse[i.sex]
            # print(data_of_people(i))
            if i.belt in self.pos[i.sex].keys():
                if name_age(ages, i.age) in self.pos[i.sex][i.belt].keys():
                    if name_weight(weights, i.age, i.weight) in self.pos[i.sex][i.belt][name_age(ages, i.age)].keys():
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)][name(i)] = i
                    else:
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)] = {}
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)][name(i)] = i
                else:
                    self.pos[i.sex][i.belt][name_age(ages, i.age)] = {}
                    if name_weight(weights, i.age, i.weight) in self.pos[i.sex][i.belt][name_age(ages, i.age)].keys():
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)][name(i)] = i
                    else:
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)] = {}
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)][name(i)] = i
            else:
                self.pos[i.sex][i.belt] = {}
                if name_age(ages, i.age) in self.pos[i.sex][i.belt].keys():
                    if name_weight(weights, i.age, i.weight) in self.pos[i.sex][i.belt][name_age(ages, i.age)].keys():
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)][name(i)] = i
                    else:
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)] = {}
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)][name(i)] = i
                else:
                    self.pos[i.sex][i.belt][name_age(ages, i.age)] = {}
                    if name_weight(weights, i.age, i.weight) in self.pos[i.sex][i.belt][name_age(ages, i.age)].keys():
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)][name(i)] = i
                    else:
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)] = {}
                        self.pos[i.sex][i.belt][name_age(ages, i.age)][name_weight(weights, i.age, i.weight)][name(i)] = i
        # print(self.pos)
        self.groups = {}
        n = 1
        for sex, dat_sex in self.pos.items():
            for belt, dat1 in dat_sex.items():
                for age, dat2 in dat1.items():
                    for weight, dat3 in dat2.items():
                        self.groups[str(n)] = {"sex": sex, "belt": belt, "age": age, "weight": weight, "peoples": {}}
                        for name_p, people in dat3.items():
                            self.groups[str(n)]["peoples"][name_p] = people
                            # print(len(self.groups[str(n)]["peoples"]), max_n, name_p, keys(dat3)[-1])
                            if len(self.groups[str(n)]["peoples"]) == max_n and (name_p != keys(dat3)[-1]):
                                n += 1
                                self.groups[str(n)] = {"sex": sex, "belt": belt, "age": age, "weight": weight, "peoples": {}}
                        n += 1


# def find(data1: Place, name1):
#     groups = data1.groups.copy()
#     out = {}
#     for ch in name1:
#         for group in groups.values():
#             for people_name in group["peoples"]:
#                 n = 0
#                 j = 0
#                 for ch2 in people_name:
#                     if ch2 == ch:
#                         j += 1
#                         n += j
#                     else:
#                         j = 0
#         if n > 0:
#             out[people_name] = n


def list_(a):
    out = []
    for k in a:
        for j in k:
            out.append(j)
    return out


def find(a, b):
    out = []
    b = b.split(";")
    b_clear = b
    b = list_(b)
    # print(b)
    if type(a) == list:
        out_prom = {}
        for j in a:
            # print(j, b_clear)
            n = 0
            for b2 in b_clear:
                if b2 not in j:
                    n += 1
            if n == len(b_clear):
                continue
            a1 = 0
            a2 = 0
            n_b = 0
            # print(j, b)
            for ch1 in j:
                for n in range(len(b) - n_b):
                    # print(j, a1, a2, ch1, b[n + n_b])
                    if ch1 == b[n + n_b]:
                        n_b = n + n_b + 1
                        a2 += 1
                        a1 += a2
                        break
                    else:
                        n_b = 0
                        a2 = 0
            out_prom[j] = a1
        for k in range(len(out_prom.values())):
            n_max = -1
            name_max = ""
            for name2, n in out_prom.items():
                if n > n_max:
                    n_max = n
                    name_max = name2
            out.append(name_max)
            del(out_prom[name_max])
        return out
    groups = a.groups.copy()
    out_prom = {}
    for j, group in groups.items():
        for people_name in group["peoples"]:
            # people_name += str(j)
            # print(j, b_clear)
            n = 0
            for b2 in b_clear:
                if b2 not in people_name:
                    n += 1
            if n == len(b_clear):
                continue
            a1 = 0
            a2 = 0
            n_b = 0
            # print(j, b)
            for ch1 in people_name:
                for n in range(len(b) - n_b):
                    # print(j, a1, a2, ch1, b[n + n_b])
                    if ch1 == b[n + n_b]:
                        n_b = n + n_b + 1
                        a2 += 1
                        a1 += a2
                        break
                    else:
                        n_b = 0
                        a2 = 0
            out_prom[f"{people_name}   {j}"] = a1
    for k in range(len(out_prom.values())):
        n_max = -1
        name_max = ""
        for name2, n in out_prom.items():
            if n > n_max:
                n_max = n
                name_max = name2
        out.append(name_max)
        del(out_prom[name_max])
    return out


def len_(mas):
    for i in mas.values():
        if i.state == False:
            return True


def compute_without_gui(path):
    open_db(path)
    return Place(peoples)


def compute():
    global data, entry_belt_main, entry_age_main, entry_weight_main, entry_people_main, label_people_data_main, entry_group_n_main, label_group_date, label_group_peoples, label_choice_age_actyal, label_choice_weight_actyal, entry_group_find, entry_sex_main
    if len(peoples) == 0 or len_(peoples):
        mb.showinfo("Так нельзя", "Введите хотя бы одного человека")
        return "No people"
    # print(int(entry_group_n.current()) + 3)
    data = Place(peoples, max_n=int(entry_group_n.current()) + 3)
#     print(data.pos)
    try:
        # print(1)
        windows["choice1"].destroy()
        windows["choice2"].destroy()
    except:
         pass
    windows["choice1"] = tkinter.Tk(className="Выбор №1 (по характеристикам)")
    choice1_frame = windows["choice1"]
    windows["choice2"] = tkinter.Tk(className="Выбор №2 (по группам)")
    choice2_frame = windows["choice2"]

    # try:
    label_choice_sex = tkinter.Label(choice1_frame, text="Пол", font=font)
    label_choice_sex.grid_configure(row=4, column=1)
    label_choice_belt = tkinter.Label(choice1_frame, text="Пояс", font=font)
    label_choice_belt.grid_configure(row=4, column=1)
    label_choice_age = tkinter.Label(choice1_frame, text="Возраст", font=font)
    label_choice_age.grid_configure(row=4, column=2)
    label_choice_age_actyal = tkinter.Label(choice1_frame, font=font)
    label_choice_age_actyal.grid_configure(row=5, column=2)
    label_choice_weight = tkinter.Label(choice1_frame, text="Вес", font=font)
    label_choice_weight.grid_configure(row=4, column=3)
    label_choice_weight_actyal = tkinter.Label(choice1_frame, font=font)
    label_choice_weight_actyal.grid_configure(row=5, column=3)
    label_choice_fio = tkinter.Label(choice1_frame, text="Человек (ФИО)", font=font)
    label_choice_fio.grid_configure(row=4, column=4)
    entry_sex_main = ttk.Combobox(choice1_frame, font=font, width=10)
    entry_sex_main["values"] = keys(data.pos)
    entry_sex_main.set(keys(data.pos)[0])
    entry_sex_main.grid_configure(row=6, column=0)
    entry_belt_main = ttk.Combobox(choice1_frame, font=font, width=25)
    k1 = keys(data.pos[keys(data.pos)[entry_sex_main.current()]])
    entry_belt_main["values"] = k1
    entry_belt_main.set(k1[0])
    entry_belt_main.grid_configure(row=6, column=1)
    entry_age_main = ttk.Combobox(choice1_frame, font=font, width=45)
    k2 = keys(data.pos[keys(data.pos)[entry_sex_main.current()]][k1[entry_belt_main.current()]])
    # k2.sort()
    # print(k2)
    entry_age_main["values"] = k2
    entry_age_main.set(k2[0])
    entry_age_main.grid_configure(row=6, column=2)
    # print(entry_age_main["values"])
    entry_weight_main = ttk.Combobox(choice1_frame, font=font, width=15)
    k3 = keys(data.pos[keys(data.pos)[entry_sex_main.current()]][k1[entry_belt_main.current()]][k2[entry_age_main.current()]])
    # k3.sort()
    # print(k3)
    entry_weight_main["values"] = k3
    entry_weight_main.set(k3[0])
    entry_weight_main.grid_configure(row=6, column=3)
    entry_people_main = ttk.Combobox(choice1_frame, font=font, width=25)
    # print(data.pos)
    k4 = keys(data.pos[keys(data.pos)[entry_sex_main.current()]][k1[entry_belt_main.current()]][k2[entry_age_main.current()]][k3[entry_weight_main.current()]])
    k4.sort()
    entry_people_main["values"] = k4
    entry_people_main.set(k4[0])
    entry_people_main.grid_configure(row=6, column=4)
    label_people_data_main = tkinter.Label(choice1_frame, font=font)
    label_people_data_main["text"] = data_of_people(data.pos[keys(data.pos)[entry_sex_main.current()]][k1[entry_sex_main.current()]][k2[entry_age_main.current()]][k3[entry_weight_main.current()]][k4[entry_people_main.current()]])
    label_people_data_main.grid_configure(row=7, column=1)
    # except Exception as e:
    #     print(e)
    #     pass

    # try:
    label_choice_belt = tkinter.Label(choice2_frame, text="№ группы:", font=font)
    label_choice_belt.grid_configure(row=0, column=0)
    entry_group_n_main = ttk.Combobox(choice2_frame, font=font)
    entry_group_n_main["values"] = keys(data.groups)
    entry_group_n_main.set(entry_group_n_main["values"][0])
    entry_group_n_main.grid_configure(row=0, column=1)
    label_group_date = tkinter.Label(choice2_frame, font=font)
    data_cur = data.groups[str(entry_group_n_main.current() + 1)]
    label_group_date["text"] = f"Пол: {data_cur['sex']}\nПояс: {data_cur['belt']}\nВозраст: {ages[data_cur['age']][0]}-{ages[data_cur['age']][1]} лет\nВес: {check_weight(weights, ages[data_cur['age']][1], data_cur['weight'], data_cur['sex'])[0]}-{check_weight(weights, ages[data_cur['age']][1], data_cur['weight'], data_cur['sex'])[1]} кг"
    label_group_date.grid_configure(row=1, column=0)
    label_group_peoples = tkinter.Label(choice2_frame, font=font)
    label_group_peoples["text"] = f'Люди:\n{print_(keys(data_cur["peoples"]))}'
    label_group_peoples.grid_configure(row=1, column=1)
    label_group_find = tkinter.Label(choice2_frame, font=font)
    label_group_find.grid_configure(row=2, column=0)
    entry_group_find = ttk.Combobox(choice2_frame, font=font, width=25)
    entry_group_find["values"] = find(data, entry_group_find.get())
    entry_group_find.grid_configure(row=2, column=1)
    # except Exception as e:
    #     print(e)
    #     pass


def print_(mas):
    out = ""
    for i in mas:
        out += f"{i}\n"
    return out


def data_of_people(people=People("?", "?", "?", "?", "?", "?", "?")):
    out = "ФИО: "
    out += f"{people.surname} {people.name} {people.last_name}\n"
    out += f"Вес: {people.weight}\n"
    out += f"Возраст: {people.age}\n"
    out += f"Пояс: {people.belt}\n"
    out += f"Пол: {people.sex}"
    return out


def rand_name():
    # out = chr(randint(65, 90))
    # for i in range(randint(1, 2)):
    #     out += chr(randint(97, 122))
    # return out
    return [choice(base_surnames), choice(base_names), choice(base_last_names)]


def name(people):
    return f"{people.surname};{people.name};{people.last_name}"


def names(array):
    out = []
    for people in array:
        out.append(f"{people.surname};{people.name};{people.last_name}")
    return out


def keys(dict_):
    out = []
    if type(dict_) == list:
        return [i for i in range(len(dict_))]
    for i in dict_.keys():
        out.append(i)
    return out


def int_(a):
    if a == "":
        return 0
    else:
        return a


def delete():
    del peoples[keys(peoples)[combobox_people.current()]]


def check_c():
    print(state.get())


def change():
    global belts, entry_surname, entry_name, entry_last_name, entry_age, entry_belt, entry_weight, entry_state, b, state
    b = keys(peoples)[combobox_people.current()]
    windows["change"] = tkinter.Tk(className="Изменение человека.")
    add_frame = tkinter.Frame(windows["change"], relief=RIDGE)
    add_frame.pack(fill=BOTH, expand=1)

    label_surname = tkinter.Label(add_frame, text=f"Фамилия", font=font)
    label_surname.grid_configure(row=0, column=0)
    label_name = tkinter.Label(add_frame, text=f"Имя", font=font)
    label_name.grid_configure(row=1, column=0)
    label_last_name = tkinter.Label(add_frame, text=f"Отчество", font=font)
    label_last_name.grid_configure(row=2, column=0)
    label_age = tkinter.Label(add_frame, text=f"Возраст", font=font)
    label_age.grid_configure(row=3, column=0)
    label_belt = tkinter.Label(add_frame, text=f"Пояс", font=font)
    label_belt.grid_configure(row=4, column=0)
    label_weight = tkinter.Label(add_frame, text=f"Вес", font=font)
    label_weight.grid_configure(row=5, column=0)
    label_state = tkinter.Label(add_frame, text=f"Подтверждение (пришёл ли)", font=font)
    label_state.grid_configure(row=6, column=0)

    entry_surname = tkinter.Entry(add_frame, font=font)
    entry_surname.insert(0, f"{peoples[keys(peoples)[combobox_people.current()]].surname}")
    entry_surname.grid_configure(row=0, column=1)
    entry_name = tkinter.Entry(add_frame, font=font)
    entry_name.insert(0, f"{peoples[keys(peoples)[combobox_people.current()]].name}")
    entry_name.grid_configure(row=1, column=1)
    entry_last_name = tkinter.Entry(add_frame, font=font)
    entry_last_name.insert(0, f"{peoples[keys(peoples)[combobox_people.current()]].last_name}")
    entry_last_name.grid_configure(row=2, column=1)
    entry_age = tkinter.Entry(add_frame, font=font)
    entry_age.insert(0, f"{peoples[keys(peoples)[combobox_people.current()]].age}")
    entry_age.grid_configure(row=3, column=1)
    entry_belt = ttk.Combobox(add_frame, font=font)
    entry_belt.insert(0, f"{peoples[keys(peoples)[combobox_people.current()]].belt}")
    entry_belt["values"] = belts
    entry_belt.set(belts[0])
    entry_belt.grid_configure(row=4, column=1)
    entry_weight = tkinter.Entry(add_frame, font=font)
    entry_weight.grid_configure(row=5, column=1)
    # state = tkinter.BooleanVar()
    # entry_state = tkinter.Checkbutton(add_frame, font=font, variable=state, onvalue=1, offvalue=0, command=check_c)
    entry_state = tkinter.Entry(add_frame, font=font)
    entry_state.grid_configure(row=6, column=1)

    add_btn = tkinter.Button(add_frame, command=add, font=font)
    add_btn["text"] = "Изменить параметры человека"
    add_btn.grid_configure(row=7)

    windows["change"].update()


def add():
    global b, entry_state
    values = [entry_surname.get(), entry_name.get(), entry_last_name.get(), entry_age.get(), belts[entry_belt.current()], entry_weight.get()]
    err = False
    for val in values:
        if val == "":
            err = True
            break
    if err:
        mb.showinfo("Что-то было введено не так.", "Какие-то ячейки пустые, чтобы продолжить заполнете их.")
        return None
    # err = False
    # print(1)
    if not (is_int(values[3]) and is_int(values[5])):
        mb.showinfo("Что-то было введено не так.", "Ячейки возраста и/или веса введены неправильно.\nВедите их в виде дробного числа через точку.")
        return None
    # try:
    values[3] = float(f"{float(values[3]):.1f}")
    values[5] = float(f"{float(values[5]):.1f}")
    nams = values[0:3]
    q = ""
    # q = int_(q) + 1
    while True:
        try:
            a = peoples[f"{nams[0]};{nams[1]};{nams[2]}{q}"]
            q = int_(q) + 1
        except:
            peoples[f"{nams[0]};{nams[1]};{nams[2]}{q}"] = People(*values)
            try:
                peoples[f"{nams[0]};{nams[1]};{nams[2]}{q}"].state = bool(entry_state.get())
            except:
                pass
            if b is not None:
                if b != f"{nams[0]};{nams[1]};{nams[2]}{q}":
                    del peoples[b]
                del b
                windows["change"].destroy()
            else:
                try:
                    windows["add"].destroy()
                except:
                    pass
            del q
            break
    # peoples[f"{entry_surname.get()};{entry_name.get()};{entry_last_name.get()}"] = People(*values)
    # mb.showinfo("Человек успешно добавлен.", "Человек успешно добавлен.")
    # windows["add"].destroy()
    # except Exception as e:
    #     mb.showinfo("Возникла ошибка.", f"{e}\n\nПожалуста, собщите об ошибке.")


def open_db_1():
    open_db(filedialog.askopenfile().name)


def open_db(path):
    global peoples
    # print(filedialog.askopenfile().name)
    data_base = DBMS.create_connection(path)
    # print(DBMS.execute_read_query(data_base, "SELECT * from competitors"))
    data_of_peoples = DBMS.execute_read_query(data_base, "SELECT * from competitors")
    # print(data_of_peoples)
    peoples = {}
    for data_ in data_of_peoples:
        q = ""
        while True:
            try:
                a = peoples[f"{data_[1]};{data_[2]};{data_[3]}{q}"]
                q = int_(q) + 1
            except:
                peoples[f"{data_[1]};{data_[2]};{data_[3]}{q}"] = People(*data_[1:9])
                del q
                break


def add_window():
    global belts, entry_surname, entry_name, entry_last_name, entry_age, entry_belt, entry_weight
    windows["add"] = tkinter.Tk(className="Добовление человека.")
    add_frame = tkinter.Frame(windows["add"], relief=RIDGE)
    add_frame.pack(fill=BOTH, expand=1)

    label_surname = tkinter.Label(add_frame, text="Фамилия", font=font)
    label_surname.grid_configure(row=0, column=0)
    label_name = tkinter.Label(add_frame, text="Имя", font=font)
    label_name.grid_configure(row=1, column=0)
    label_last_name = tkinter.Label(add_frame, text="Отчество", font=font)
    label_last_name.grid_configure(row=2, column=0)
    label_age = tkinter.Label(add_frame, text="Возраст", font=font)
    label_age.grid_configure(row=3, column=0)
    label_belt = tkinter.Label(add_frame, text="Пояс", font=font)
    label_belt.grid_configure(row=4, column=0)
    label_weight = tkinter.Label(add_frame, text="Вес", font=font)
    label_weight.grid_configure(row=5, column=0)

    entry_surname = tkinter.Entry(add_frame, font=font)
    entry_surname.grid_configure(row=0, column=1)
    entry_name = tkinter.Entry(add_frame, font=font)
    entry_name.grid_configure(row=1, column=1)
    entry_last_name = tkinter.Entry(add_frame, font=font)
    entry_last_name.grid_configure(row=2, column=1)
    entry_age = tkinter.Entry(add_frame, font=font)
    entry_age.grid_configure(row=3, column=1)
    entry_belt = ttk.Combobox(add_frame, font=font)
    entry_belt["values"] = belts
    # entry_belt.set(belts[0])
    entry_belt.grid_configure(row=4, column=1)
    entry_weight = tkinter.Entry(add_frame, font=font)
    entry_weight.grid_configure(row=5, column=1)

    add_btn = tkinter.Button(add_frame, command=add, font=font)
    add_btn["text"] = "Добавить человека"
    # add_btn.pack()
    add_btn.grid_configure(row=6)

    windows["add"].update()


# peoples[""] = People(1, 1, 1, 1, 1, 1)


# print(find(["abccde", "abcde", "edcba", "qwerty", "bcd"], "bcd"))

# data_base = DBMS.create_connection(filedialog.askopenfile().name)
# DBMS.execute_query(data_base, "DELETE FROM competitors WHERE id >= 0")
# DBMS.execute_query(data_base, "DROPTABLE competitors")
# DBMS.execute_query(data_base, """CREATE TABLE IF NOT EXISTS competitors (
#   id INTEGER PRIMARY KEY,
#   surname TEXT,
#   name TEXT,
#   last_name TEXT,
#   age FLOAT,
#   belt TEXT,
#   weight FLOAT,
#   sex TEXT
# );""")
# for i in range(150):
#     rand_nam = rand_name()
#     DBMS.execute_query(data_base, f"""
#         INSERT INTO
#             competitors (id, surname, name, last_name, age, belt, weight, sex)
#         VALUES
#             ({randint(0, 1e10)}, {rand_nam[0]}, {rand_nam[1]}, {rand_nam[2]}, {randint(40, 790) / 10}, {belts[randint(0, 16)]}, {randint(150, 950) / 10}, {choice(["Men", "Women"])});
#         """)


for i in range(150):
    nams = rand_name()
    q = ""
    # q = int_(q) + 1
    while True:
        try:
            a = peoples[f"{nams[0]};{nams[1]};{nams[2]}{q}"]
            q = int_(q) + 1
        except:
            peoples[f"{nams[0]};{nams[1]};{nams[2]}{q}"] = People(*nams, choice(["Мужской", "Женский"]), randint(4, 79), randint(150, 950) / 10, belts[randint(0, 16)], True)
            del(q)
            break


if __name__ == "__main__":
    main_frame = tkinter.Frame(windows["main"], relief=RIDGE)
    main_frame.pack(fill=BOTH, expand=1)

    combobox_people = ttk.Combobox(main_frame, font=font, width=25)
    combobox_people["values"] = peoples.keys()
    combobox_people.set("")
    combobox_people.grid_configure(row=0, column=0)

    label_people_data = tkinter.Label(main_frame, font=font, text=data_of_people())
    label_people_data.grid_configure(row=1)

    btn_add = tkinter.Button(main_frame, command=add_window, font=font)
    btn_add["text"] = "Добавить человека"
    btn_add.grid_configure(row=2)

    label_group_n = tkinter.Label(main_frame, font=font, text="Макс. чел. в группе")
    label_group_n.grid_configure(row=3, column=1)

    label_group_n = tkinter.Label(main_frame, font=font, text=f"Зарегестрированно: {len(peoples)}")
    label_group_n.grid_configure(row=0, column=1)

    # dlg = Open(master=main_frame, filetypes=[('Python files', '*.py'), ('All files', '*')])
    # fl = dlg.show()
    # path = filedialog.askopenfilename()

    btn_add = tkinter.Button(main_frame, command=open_db_1, font=font)
    btn_add["text"] = "Открыть базу"
    btn_add.grid_configure(row=3, column=0)

    entry_group_n = ttk.Combobox(main_frame, font=font)
    entry_group_n["values"] = ["3", "4", "5", "6", "7"]
    entry_group_n.set("3")
    entry_group_n.grid_configure(row=4, column=1)

    btn_add = tkinter.Button(main_frame, command=compute, font=font)
    btn_add["text"] = "Расчитать"
    btn_add.grid_configure(row=4)
    btn_change = tkinter.Button(main_frame, command=change, font=font)
    btn_change["text"] = "Изменить"
    btn_change.grid_configure(row=1, column=1)
    btn_del = tkinter.Button(main_frame, command=delete, font=font)
    btn_del["text"] = "Удалить"
    btn_del.grid_configure(row=2, column=1)
    while True:
        try:
            # print(data(peoples[keys(peoples)[combobox_people.current()]]))
            label_people_data["text"] = data_of_people(peoples[keys(peoples)[combobox_people.current()]])
        except:
            label_people_data["text"] = data_of_people()
        # label_people_data.grid_configure(row=1)
        # label_people_data.update()
        # print(keys(peoples))
        combobox_people["values"] = find(keys(peoples), combobox_people.get())
        label_group_n["text"] = f"Зарегестрированно: {len(peoples)}"
        # try:
        #     windows["change"].update()
        #     print(entry_state.instate([1]))
        # except Exception as e:
        #     print(e)
        #     pass
        try:
            data_cur = data.groups[str(entry_group_n_main.current() + 1)]
            label_group_date["text"] = f"Пол: {data_cur['sex']}\nПояс: {data_cur['belt']}\nВозраст: {ages[data_cur['age']][0]}-{ages[data_cur['age']][1]} лет\nВес: {check_weight(weights, ages[data_cur['age']][1], data_cur['weight'], data_cur['sex'])[0]}-{check_weight(weights, ages[data_cur['age']][1], data_cur['weight'], data_cur['sex'])[1]} кг"
            label_group_peoples["text"] = f'Люди:\n{print_(keys(data_cur["peoples"]))}'
            entry_group_find["values"] = find(data, entry_group_find.get())
            # print(f"Возраст: {ages[data_cur['age']][0]}-{ages[data_cur['age']][1]} лет")
        except Exception as e:
            # print(e)
            pass
        try:
            k1 = keys(data.pos[keys(data.pos)[entry_sex_main.current()]])
            entry_belt_main["values"] = k1
            k2 = keys(data.pos[keys(data.pos)[entry_sex_main.current()]][k1[entry_belt_main.current()]])
            entry_age_main["values"] = k2
            k3 = keys(data.pos[keys(data.pos)[entry_sex_main.current()]][k1[entry_belt_main.current()]][k2[entry_age_main.current()]])
            entry_weight_main["values"] = k3
            k4 = keys(data.pos[keys(data.pos)[entry_sex_main.current()]][k1[entry_belt_main.current()]][k2[entry_age_main.current()]][k3[entry_weight_main.current()]])
            entry_people_main["values"] = k4
            data_cur = data.pos[keys(data.pos)[entry_sex_main.current()]][k1[entry_sex_main.current()]][k2[entry_age_main.current()]][k3[entry_weight_main.current()]][k4[entry_people_main.current()]]
            label_people_data_main["text"] = data_of_people(data_cur)
            age = k2[entry_age_main.current()]
            weight = k3[entry_weight_main.current()]
            label_choice_age_actyal["text"] = f"{ages[age][0]}-{ages[age][1]}"
            label_choice_weight_actyal["text"] = f"{check_weight(weights, ages[age][1], weight, data_cur.sex)[0]}-{check_weight(weights, ages[age][1], weight, data_cur.sex)[1]}"
        except Exception as e:
            # print(e)
            pass
        main_frame.update()