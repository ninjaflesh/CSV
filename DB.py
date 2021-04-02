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


#sql.execute("""DELETE FROM users WHERE user_id >= 0""")

t1 = User('Admin', "admin")
t1.check_login()

t2 = User('Admin', "Admin")
t2.check_login()

t3 = User('Admin_logi', "admin")
t3.check_login()
