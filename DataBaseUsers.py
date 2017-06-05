import sqlite3
from print_sqlite2 import *
from User import *
import random
import string
#http://stackoverflow.com/questions/13709482/how-to-read-text-file-in-javascript


class DataBaseUsers():
    def __init__(self):
        self.table_path = "users/users.db"
        self.conn = sqlite3.connect(self.table_path, check_same_thread=False)
        self.c = self.conn.cursor()

    def create_table(self):
        try:
            self.c.execute('''CREATE TABLE users(name text, hash_pass text, email text, id text, key text, second_pass text)''')
            return True
        except Exception:
            return False

    def insert_user(self, user):
        """
        The function adds a new user to the database if the new user's email address is not used.
        """
        name = user.get_name()
        hash_pass = user.get_hashpass()
        email = user.get_email()
        id = user.get_id()
        t = (email,)
        self.c.execute('SELECT * FROM users WHERE email=?', t)
        if self.c.fetchone():
            return "Sorry but this email is already used"
        key = self.generate_key()
        second_pass = self.generate_key()
        self.c.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", (name, hash_pass, email, id, key, second_pass))
        self.conn.commit()

    def generate_key(self):
        master = string.ascii_letters+string.digits
        password = ""
        for i in range(0, 32):
            password += random.choice(master)
        return password

    def print_table(self):
        self.c.execute("SELECT * FROM users")
        data = self.c.fetchall()
        print data

    def delete_table(self):
        self.c.execute("DROP table if exists users")
        self.conn.commit()

    def delete_user(self):
        pass

    def authenticate(self, email, password):
        self.c.execute("SELECT * FROM users WHERE hash_pass=? AND email=?", (password, email))
        if self.c.fetchone():
            return True
        return False

    def get_user_by_email(self, email):
        user_line = self.c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchall()
        if user_line:
            return User(user_line[0][0], user_line[0][1], user_line[0][2], user_line[0][3])

    def get_user_by_id(self, id):
        user_line = self.c.execute("SELECT * FROM users WHERE id=?", (id,)).fetchall()
        if user_line:
            return User(user_line[0][0], user_line[0][1], user_line[0][2], user_line[0][3])

    def get_users_id(self):
        return self.c.execute("SELECT id FROM users").fetchall()

    def check_email(self, email):
        t = (email,)
        if self.c.execute("SELECT * FROM users WHERE email=?", t).fetchall():
            return False
        return True

    def get_username_by_id(self, id_to_search):
        username = self.c.execute("SELECT name FROM users WHERE id=?", (id_to_search,)).fetchone()
        if username:
            return username[0]

    def get_key_by_email(self, email):
        t = (email, )
        self.c.execute("SELECT key FROM users WHERE email=?", t)
        key = self.c.fetchone()
        print key
        return key

    def check_authentication(self, email, second_pass):
        self.c.execute("SELECT * FROM users WHERE email=? AND second_pass=?", (email, second_pass))
        if self.c.fetchone():
            return True
        return False

    def change_key(self, email):
        t = (email, )
        if self.c.execute("SELECT * FROM users WHERE email=?", t).fetchone():
            new_key = self.generate_key()
            t = (new_key, email)
            self.c.execute("UPDATE users SET key=?  WHERE email=?", t)
            self.conn.commit()
            return new_key
        return False

if __name__ == "__main__":
    db = DataBaseUsers()
    db.delete_table()
    db.create_table()
    db.insert_user(User("Tamir", "1234", "cren@g", "1"))
    db.print_table()

    a="""c.execute("DROP table if exists users")
    conn.commit()
    printing()"""