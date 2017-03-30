
import sqlite3


class DataBaseFiles():
    def __init__(self):
        self.table_path = "users/files.db"
        self.conn = sqlite3.connect(self.table_path)
        self.c = self.conn.cursor()

    def create_table(self):
        try:
            self.c.execute('''CREATE TABLE files (user_file_name TEXT, server_file_name TEXT)''')
            return True
        except Exception:
            return False

    def insert_file(self, user_file_name, server_file_name):
        """
        The function adds a new file to the database, if the user_file_name is already used the
        function return false.
        """
        t = (user_file_name,)
        self.c.execute('SELECT * FROM files WHERE user_file_name=?', t)
        if self.c.fetchone():
            return False
        self.c.execute("INSERT INTO files VALUES (?,?)", (user_file_name, server_file_name))
        self.conn.commit()
        return True

    def print_table(self):
        self.c.execute("SELECT * FROM files")
        data = self.c.fetchall()
        print data

    def delete_table(self):
        self.c.execute("DROP table if exists files")
        self.conn.commit()

    def delete_file(self, user_file_name):
        t = (user_file_name,)
        self.c.execute('DELETE * FROM files WHERE user_file_name=?', t)
        return True

    def authenticate(self, email, password):
        self.c.execute("SELECT * FROM users WHERE hash_pass=? AND email=?", (password, email))
        if self.c.fetchone():
            return True
        return False

    def get_user_by_email(self, email):
        user_line = self.c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchall()
        if user_line:
            print user_line
            return User(user_line[0][0], user_line[0][1], user_line[0][2], user_line[0][3])

    def get_user_by_id(self, id):
        user_line = self.c.execute("SELECT * FROM users WHERE id=?", (id,)).fetchall()
        if user_line:
            print user_line
            return User(user_line[0][0], user_line[0][1], user_line[0][2], user_line[0][3])

if __name__ == "__main__":
    db = DataBaseUsers()
    db.delete_table()
    db.create_table()
    db.insert_user(User("Tamir", "1234", "cren@g", "33"))
    db.print_table()

    a="""c.execute("DROP table if exists users")
    conn.commit()
    printing()"""