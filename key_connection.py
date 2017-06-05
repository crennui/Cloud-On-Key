__author__ = 'Tamir'
import httplib
import webbrowser
import wx
import os
import random
import struct
from Crypto.Cipher import AES


def ask(message=""):
    dlg = wx.TextEntryDialog(None, message, "")
    dlg.ShowModal()
    result = dlg.GetValue()
    dlg.Destroy()
    return result


def gui_get_email(text):
    # Initialize wx App
    app = wx.App()
    app.MainLoop()

    # Call Dialog
    x = ask(message=text)
    return x


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename.split(".")[0] + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    print "I AM HERE"
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
        print out_filename

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


conn = httplib.HTTPSConnection("127.0.0.1:5000")
email = gui_get_email('Welcome to Cloud on key. please enter your Email')
conn.request("POST", "/login_key", email)
r1 = conn.getresponse()
data1 = r1.read()
decrypt_file(data1, "second_password.enc", "second_password.txt")
file_pass = open("second_password.txt", "rb")
second_pass = file_pass.read()
file_pass.close()
data = str(email) + " " + second_pass
os.remove("second_password.enc")
conn.request("POST", "/secret_password", data)
r2 = conn.getresponse()
data2 = r2.read()
encrypt_file(data2, "second_password.txt")
os.remove("second_password.txt")
conn.close()
webbrowser.open_new_tab("https://127.0.0.1:5000/login")