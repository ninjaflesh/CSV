import sqlite3
from time import gmtime, strftime
from random import randint

global db
global sql

db = sqlite3.connect('server')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    time TEXT,
    login TEXT,
    password TEXT,
    cash BIGINT
)""")

db.commit()


def regist():
    create_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    user_login = input('Login: ')
    user_password = input('Password: ')

    sql.execute("SELECT login FROM users WHERE login = '{user_login}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)",
                    (create_time, user_login, user_password, 0))
        db.commit()

        print('Запись создана.')
    else:
        print('Запись уже существует.')

        for value in sql.execute("SELECT * FROM users"):
            print(value)


def delete_db():
    sql.execute(f'DELETE FROM users WHERE login = "{user_login}"')
    db.commit()
    print('Запись удалена!')


def money():
    global user_login
    user_login = input("Log in: ")
    number = randint(1, 2)

    for i in sql.execute(f'SELECT cash FROM users WHERE login = "{user_login}"'):
        balance = i[0]

    sql.execute(f'SELECT login FROM users WHERE login = "{user_login}"')
    if sql.fetchone() is None:
        print("Логина не существует.")
        regist()
    else:
        if number == 1:
            sql.execute(
                f'UPDATE users SET cash = {1000 + balance} WHERE login = "{user_login}"')
            db.commit()
            print("Вы выиграли!")
            enter()
        else:
            print("Вы проиграли.")
            delete_db()


def enter():
    for i in sql.execute('SELECT time, login, cash FROM users'):
        print(i)


def main():
    money()


main()
