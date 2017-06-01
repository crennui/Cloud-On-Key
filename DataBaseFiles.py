#---------------------------------IMPORTS-------------------------------------
import random
import sqlite3
from string import letters
import os
import win32com.client
import mammoth

#------------------------------CONSTANTS---------------------------------------
FILES_PATH = os.path.dirname(os.path.abspath(__file__))+"/files/"
CREATE_PERMISSIONS = '''CREATE TABLE permissions
 (user_id TEXT, user_file_name TEXT ,server_file_name TEXT, permission_type TEXT, owner TEXT)'''
#-------------------------------------------------------------------------


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

    def insert_file(self, owner, user_file_name, data=""):
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
            f.write(data)
            f.close()
            return True
        except Exception:
            return False

    def print_table(self):
        self.c.execute("SELECT * FROM files")
        data = self.c.fetchall()
        print data

    def delete_files_table(self):
        self.c.execute("DROP table if exists files")
        self.conn.commit()

    def delete_permission_table(self):
        self.c.execute("DROP table if exists permissions")
        self.conn.commit()

    def delete_file(self, server_file_name, user_id):
        t = (server_file_name, user_id)
        self.c.execute('DELETE FROM files WHERE server_file_name=? AND owner=?', t)
        self.c.execute('DELETE FROM permissions WHERE server_file_name=? AND user_id=?', t)
        os.remove(FILES_PATH+server_file_name)
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
        """
        returns a list of the user_file_name of all the files with the user
        owned or shared with.
        """
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

    def html_to_word(self, server_file_name, user_file_name):
        word = win32com.client.Dispatch('Word.Application')
        doc = word.Documents.Add(FILES_PATH+server_file_name)
        print FILES_PATH+user_file_name.split(".")[0]+'.docx'
        doc.SaveAs2(FILES_PATH+user_file_name.split(".")[0]+'.docx', FileFormat=12)
        doc.Close()
        word.Quit()
        return True

    def word_to_html(self, owner, new_file_name):
        with open(FILES_PATH+new_file_name, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
        html = result.value
        #messages = result.messages
        end_with = ".txt"
        file_end = new_file_name.split(".")[1]
        if file_end != ".docx":
            end_with = file_end
        self.insert_file(owner, new_file_name.split(".")[0]+end_with)
        print html


def reset_tables():
    db = DataBaseFiles()
    db.delete_files_table()
    db.delete_permission_table()
    db.create_table()
    db.create_permissions_table()
    #db.add_permission("33", "hello.txt", "j154.txt", "r", "36")
    db.print_table()

if __name__ == "__main__":
    #reset_tables()
    #db.html_to_word("g74.txt", "madara.txt")
    a="""c.execute("DROP table if exists users")
    conn.commit()
    printing()"""