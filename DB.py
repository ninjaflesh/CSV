import sqlite3
import bcrypt
from time import gmtime, strftime

# Подключение к БД
with sqlite3.connect('server.db') as db:
    sql = db.cursor()


class User:  # Клас User, принемает логин и пароль
    def __init__(self, login: str, password: str):
        self.user_login = login
        self.user_password = password
        self.create_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    # Метод шифрует пароль
    def get_hashed_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Метод шифрует пароль и проверяет с ранее шифрованным
    def check_password(self, hash_p):
        return bcrypt.checkpw(self.user_password.encode('utf-8'), hash_p)

    # Метод проверяет логин на сущестование
    def check_login(self):
        sql.execute(
            f"SELECT login, password FROM users WHERE login = '{self.user_login}'")
        coll = sql.fetchone()
        if coll is not None:
            if self.check_password(coll[1]):
                print('Вы успешно авторизовались.')
                self.edit_schedule()
            else:
                print("Не верный логин или пароль.")
        else:
            print("Создайте новую запись.")
            self.register()  # Отправляем на регистрацию

    # Метод регистрирует пользователя
    def register(self):
        new_login = input('Введите логи для регистрации: ')

        sql.execute(
            f"SELECT login FROM users WHERE login = '{new_login}'")
        if sql.fetchone() is None:
            new_password = input('Введите пароль для регистрации: ')

            sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)",
                        (None, new_login, self.get_hashed_password(new_password), self.create_time))
            db.commit()
            print('Запись создана.')
        else:
            print('Логин занят.')

    # Метод позволяющий пользователю взаимодействовать с расписанием.
    def edit_schedule(self):
        print("Для создания занятия введите: 1\nДля редактирования занятия введите: 2\n"
              "Для удаления занятия введите: 3\nДля создания таблицы с расписанием введите: 4")
        check = int(input('Выберите действие: '))

        if check == 1:
            create_lesson()
        elif check == 2:
            edit_lesson()
        elif check == 3:
            delete_lesson()
        elif check == 4:
            build_schedule()
        else:
            print("Я тебя не понимаю О_о")


def create_lesson():
    group = input('Введите название группы: ')
    teacher = input('Введите ФИО преподователя: ')
    work = input('Введите название предмета: ')
    print("Если аудитория является классом, введите: 1\nЕсли аудитория является спортзалом, введите: 2\n"
          "Если аудитория является лабораторией, введите: 3")
    check = int(input('Введите тип аудитории: '))
    audience = input('Введите номер аудитории: ')

    if check == 1:
        a_type = "Класс"
    elif check == 2:
        a_type = "Спортзал"
    elif check == 3:
        a_type = "Лаборатория"
    else:
        print("Я тебя не понимаю О_о")

    sql.execute(f"INSERT INTO timetable VALUES (?, ?, ?, ?, ?, ?)",
                (None, group, teacher, work, audience, a_type))
    db.commit()
    print("Занятие создано.")


def edit_lesson():
    sql.execute(f"SELECT * FROM timetable ")
    for x in sql.fetchall():
        print(x)
    id = int(input("Укажите id предмета для редакции: "))
    print("Для изменения группы, введите: 1\nДля изменения препопдователя, введите: 2\n"
          "Для изменения предмета, введите: 3\nДля изменения аудитории, введите 4\n"
          "Для изменения номера аудитории, введите 5")
    colom = int(input("Укажите номер колонны: "))
    if colom == 1:
        value = input("Введите новое название группы: ")
        colom = "group"
    elif colom == 2:
        value = input("Введите новое имя преподователя: ")
        colom = "teacher"
    elif colom == 3:
        value = input("Введите новое название предмета: ")
        colom = "work"
    elif colom == 4:
        value = input("Введите новое название аудитории: ")
        colom = "audience"
    elif colom == 5:
        print("Если аудитория является классом, введите: 1\nЕсли аудитория является спортзалом, введите: 2\n"
              "Если аудитория является лабораторией, введите: 3")
        check = int(input('Введите тип аудитории: '))
        if check == 1:
            value = "Класс"
            colom = "type"
        elif check == 2:
            value = "Спортзал"
            colom = "type"
        elif check == 3:
            value = "Лаборатория"
            colom = "type"
        else:
            print("Я тебя не понимаю О_о")
    else:
        print("Я тебя не понимаю О_о")

    sql.execute(
        f"UPDATE timetable SET '{colom}'='{value}' WHERE timetable_id = '{id}'")
    db.commit()
    print("Занятие отредактированно.")


def delete_lesson():
    sql.execute(f"SELECT * FROM timetable ")
    for x in sql.fetchall():
        print(x)
    id = int(input("Укажите id предмета для удаления: "))
    sql.execute(f"DELETE FROM timetable WHERE timetable_id = '{id}'")
    db.commit()
    print("Занятие удалено.")


def build_schedule():
    None


t1 = User('Admin', "admin")
t1.check_login()
