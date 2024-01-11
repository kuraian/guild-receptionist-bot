import sqlite3
from sqlite3 import Error
import datetime


def create_connection(db_file):
    """
    create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def init_users_db():
    """
    create a SQLite database containing users
    :return: None
    """
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS users(
        id integer PRIMARY KEY,
        created_date text,
        url text
        ) """
    cur.execute(sql)
    conn.commit()
    return None


def create_user(user):
    """
    inserts a user into users.db and creates an SQLite db for an individual user
    :param user: unique user id integer
    :return: boolean
    """

    init_users_db()

    if check_user(user):
        return False
    conn = create_connection("users.db")
    cur = conn.cursor()

    sql = """INSERT or IGNORE INTO users(id, created_date, url) VALUES(?, ?, ?)"""
    cur.execute(sql, (user, datetime.date.today(), "na"))
    conn.commit()

    conn = create_connection(str(user) + ".db")
    cur = conn.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL,
            description text NOT NULL,
            created_date text,
            due_date text,
            completed_date text,
            is_active integer NOT NULL,
            priority_level integer
            )
            """
    )
    print("created")
    conn.commit()
    return True


def check_user(user):
    """
    checks if a user exists in users.db
    :param user: unique user's id
    :return: boolean
    """

    conn = create_connection("users.db")
    cur = conn.cursor()

    sql = """SELECT id FROM users WHERE id=?"""
    return len(cur.execute(sql, (user,)).fetchall()) != 0


def create_task(user, args):
    """
    inserts a user into users.db and creates an SQLite db for an individual user
    :param user: unique user id integer
    :return: boolean
    """
    conn = create_connection(str(user) + ".db")
    cur = conn.cursor()

    sql = """INSERT or IGNORE INTO tasks(name, description, created_date, due_date, completed_date, is_active, priority_level) VALUES(?, ?, ?, ?, ?, ?, ?)"""
    params = (args[0], args[1], datetime.date.today(), args[2], "na", True, args[3])
    cur.execute(sql, params)
    conn.commit()


def active_tasks(user):
    conn = create_connection(str(user) + ".db")
    cur = conn.cursor()

    sql = """SELECT * FROM tasks WHERE is_active=1"""
    cur.execute(sql)
    rows = cur.fetchall()

    return rows


def complete_task(user, arg):
    conn = create_connection(str(user) + ".db")
    cur = conn.cursor()

    sql = """UPDATE tasks SET is_active = 0, completed_date = ? WHERE id = ?"""
    cur.execute(sql, (datetime.date.today(), arg))
    conn.commit()
