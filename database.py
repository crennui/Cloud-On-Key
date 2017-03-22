import sqlite3
from print_sqlite2 import *


class DataBaseUsers:
    def __init__(self):
        self.table_path = "users/users.db"
        self.conn = sqlite3.connect(self.table_path)
        self.c = self.conn.cursor()

    def create_table(self):
        try:
            self.c.execute('''CREATE TABLE users(name text, hash_pass text, email text, id text)''')
            return True
        except Exception:
            return False

    def insert_user(self, user):
        """
        The function adds a new user to the database if the new user's email address is not used.
        """
        name = user.get_name()
        hash_pass = user.get_password()
        email = user.get_email()
        id = user.get_id()
        t = (email,)
        self.c.execute('SELECT * FROM users WHERE email=?', t)
        if self.c.fetchone():
            return "Sorry but this email is already used"
        self.c.execute("INSERT INTO users VALUES (?,?,?,?)", (name, hash_pass, email, id))
        self.conn.commit()

    def print_table(self):
        self.c.execute("SELECT * FROM users")
        data = self.c.fetchall()
        print data

    def delete_table(self, table):
        self.c.execute("DROP table if exists ", (table))
        self.conn.commit()

    def delete_user(self):
        pass

db = DataBaseUsers()
db.insert_user("Tamir", "1234", "cren@g", "33")
db.print_table()
db.delete_table("users")

a="""c.execute("DROP table if exists users")
conn.commit()
printing()"""