__author__ = 'Tamir'

import os
import random
import zipfile
import shutil
import struct
from Crypto.Cipher import AES


def zipdir(path, ziph):
    # ziph is zipfile handle
    print "hiiiiiii"
    for root, dirs, files in os.walk(path):
        print files + " " + root + " " + dirs
        for file in files:
            ziph.write(os.path.join(root, file))


def zip_folder():
    zipf = zipfile.ZipFile('madara.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('/files', zipf)
    zipf.close()


def mad():
    zfName = 'simonsZip.kmz'
    foo = zipfile.ZipFile(zfName, 'w')
    foo.write("temp.kml")
    # Adding files from directory 'files'
    for root, dirs, files in os.walk('files'):
        for f in files:
            foo.write(os.path.join(root, f))
    foo.close()
    os.remove("temp.kml")


def hla():
    shutil.make_archive("files/hello", "zip", "files/madara")


def copy():
    shutil.copyfile("E:/bla/hi.txt", "bg.txt")


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


def make_dir():
    os.makedirs("files/jeez")
    working_file = open("files/jeez/madara.txt", "w")
    working_file.write("hello")
    working_file.close()
    encrypt_file()
make_dir()