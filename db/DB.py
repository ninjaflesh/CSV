import sqlite3
from time import gmtime, strftime

with sqlite3.connect('server.db') as db:
    sql = db.cursor()

    # Создание таблицы users
    sql.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        login TEXT,
        password TEXT,
        time TEXT
        )""")

    db.commit()


class User:  # Клас User, принемает логин и пароль
    def __init__(self, login, password):
        self.user_login = login
        self.user_password = password
        self.create_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    # Метод проверяет логин на сущестование и создает запись если логин не занят
    def check_login(self):
        sql.execute(
            f"SELECT login FROM users WHERE login = '{self.user_login}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)",
                        (None, self.user_login, self.user_password, self.create_time))
            db.commit()

            print('Запись создана.')
        else:
            print("Создайте новую запись.")


x = User('Dima', 123)
x.check_login()
