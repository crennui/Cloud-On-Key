import random
import sqlite3
from string import letters
CREATE_PERMISSIONS = '''CREATE TABLE permissions
 (user_id TEXT, user_file_name TEXT ,server_file_name TEXT, permission_type TEXT, owner TEXT)'''


class DataBaseFiles():
    def __init__(self):
        self.table_path = "users/files.db"
        self.conn = sqlite3.connect(self.table_path)
        self.c = self.conn.cursor()

    def create_table(self):
        """
        The function creates a table by the name files in the table_path file. 
        """
        try:
            self.c.execute('''CREATE TABLE files (owner TEXT, user_file_name TEXT, server_file_name TEXT)''')
            return True
        except Exception:
            return False

    def create_permissions_table(self):
        """
        The function creates a table by the name permissions in the table_path file.
        """
        try:
            self.c.execute(CREATE_PERMISSIONS)
            return True
        except Exception:
            return False

    def add_permission(self, user_id, user_file_name, server_file_name, permission_type, owner):
        t = (user_id, user_file_name, server_file_name, permission_type, owner)
        self.c.execute("INSERT INTO permissions VALUES(?,?,?,?,?)", t)
        self.conn.commit()

    def insert_file(self, owner, user_file_name):
        """
        The function adds a new file to the database, if the user_file_name is already used the
        function return false.
        """
        try:
            server_file_name = self.generate_name() + "." + user_file_name.split(".")[1]
            print server_file_name
            t = (owner, user_file_name, server_file_name)
            self.c.execute("INSERT INTO files VALUES (?,?,?)", t)
            self.conn.commit()
            f = open("files/"+server_file_name, "w")
            f.close()
            return True
        except Exception:
            return False

    def print_table(self):
        self.c.execute("SELECT * FROM files")
        data = self.c.fetchall()
        print data

    def delete_table(self):
        self.c.execute("DROP table if exists permissions")
        self.conn.commit()

    def delete_file(self, user_file_name):
        t = (user_file_name,)
        self.c.execute('DELETE FROM files WHERE user_file_name=?', t)
        self.conn.commit()
        return True

    def get_files_by_owner_id(self, owner):
        """
        returns a list of the files the user owned (The names that the user gave).
        None if no files are found.
        """
        t = (owner,)
        return self.c.execute('SELECT * FROM files WHERE owner=?', t).fetchall()

    def generate_name(self):
        """
        The function returns a random name of a file.
        The name has to start with a letter, and then a number between 0 and 1000.
        The name can only appear once in the server.
        """
        server_file_name = random.choice(letters)
        server_file_name += str(random.randint(0, 1000))
        s_f_n = (server_file_name,)
        while self.c.execute('SELECT * FROM files WHERE server_file_name=?', s_f_n).fetchone():
            server_file_name = random.choice(letters)
            server_file_name += random.randint(0, 1000)
            s_f_n = (server_file_name,)
        return server_file_name

    def get_user_files_list(self, user_id):
        t = (user_id, )
        list_of_files = self.c.execute("SELECT * FROM files WHERE owner=?", t).fetchall()
        list_of_files_not_owned = self.c.execute("SELECT * FROM permissions WHERE user_id=?", t).fetchall()
        return [file_name[1] for file_name in list_of_files] + [file_name[1] for file_name in list_of_files_not_owned]

    def user_to_server_file_name_owned(self, user_file_name, user_id):
        t = (user_file_name, user_id)
        return self.c.execute("SELECT server_file_name FROM files WHERE user_file_name=? AND owner=?", t).fetchone()

    def user_to_server_file_name_not_owned(self, user_file_name, user_id):
        t = (user_file_name, user_id)
        return self.c.execute("SELECT server_file_name FROM permissions WHERE user_file_name=? AND user_id=?", t).fetchone()

if __name__ == "__main__":
    db = DataBaseFiles()
    db.delete_file("hi.txt")
    db.print_table()

    a="""c.execute("DROP table if exists users")
    conn.commit()
    printing()"""