__author__ = 'Tamir'
import win32com.client
import mammoth
import subprocess
import pypandoc


def html_to_word():
    word = win32com.client.Dispatch('Word.Application')
    doc = word.Documents.Add('C:/CyberProjects/cloud_on_key/Cloud-On-Key/files/g74.txt')
    doc.SaveAs2('hello2.docx', FileFormat=12)
    doc.Close()
    word.Quit()
    #subprocess.call(['soffice', '--headless', '--convert-to', 'docx', "hello2.doc"])
    return


def g():
    out = pypandoc.convert(source="files/log_in.html", format="html", to='docx', outputfile='pls.docx', extra_args=['-RTS'])
    print out


def word_to_html(file_name):
    print "k"
    with open("C:/CyberProjects/cloud_on_key/Cloud-On-Key/"+file_name, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
    html = result.value
    messages = result.messages
    print html

html_to_word()
