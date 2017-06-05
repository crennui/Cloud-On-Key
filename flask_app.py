__author__ = 'Tamir'

import random
import os
from flask import Flask
from flask import send_file, render_template, request, Response, redirect, session, send_from_directory, g
from flask_login import LoginManager, login_required, login_user, logout_user
from DataBaseUsers import *
from DataBaseFiles import *
from flask_socketio import SocketIO, emit, join_room, leave_room

data_base = DataBaseUsers()
data_base_files = DataBaseFiles()
OK = "OK - 200"

#------------------------------ROUTES----------------------------------------------
UPDATE_ROUTE = 'update'
TEXT_EDITOR_ROUTE = "/text_editor"
USER_ROUTE = "/<user>"
HOMEPAGE_ROUTE = "/"
FILES_ROUTE = "/files"
LOGIN_ROUTE = "/login"
GET_IMAGE_ROUTE = '/get_image/<image_name>'
LOGOUT_ROUTE = "/logout"
REGISTER_ROUTE = "/register"
FILE_REQUEST_ROUTE = "/file_request/<file_name>"
#------------------------------PATHS----------------------------------------------
TEXT_EDITOR_PATH = "text_editor.html"
STATIC_PATH = "/static/"
LOGIN_PAGE_PATH = "login_page.html"
FILES_PATH = "files/"
FILES_VIEW_PATH = "files_view.html"
HOMEPAGE_PATH = "index.html"

#-----------------------------SOCKET-ROUTS-----------------------------------------
CREATE_FILE = "create_file"

#-----------------------------CONSTANTS--------------------------------------------
ERROR_404 = "HTTP/1.0 404 Not Found"
ERROR_MSG = "Sorry your email or password are not correct"
ERROR_MSG_ALREADY_USED = "This Email is already used"
ERROR_MSG_LOGOUT = "you are logged out"
METHOD_POST = "POST"
METHOD_GET = "GET"
SECRET_KEY = "secret"
EMAIL = 'email'
PASSWORD = 'password'
UPDATE_ACTION = 'update'
WORKING_FILE = "working_file"
WRITE_ACTION = 'w'
READ_B_ACTION = "rb"
USER_ID = 'user_id'
HTML_FILE_TEMPLATE = """ <a href="/file_request/%s">
                            <div class="img-single">
                            <img src="static/document_file_icon_2.png">
                            <h3>%s</h3>
                            </div></a>"""
USER_NAMESPACE = "user_namespace"
#--------------------------------popup-messages----------------------------------------
POPUP_MSG = 'popup-msg'
ALREADY_USED = "The file name is already used !"
DELETED = "The file %s deleted !"
#----------------------------------------------------------------------------
app = Flask(__name__)
#-------------------------------------SocketIO----------------------------------
#app.config['SECRET_KEY'] = SECRET_KEY
socket = SocketIO(app)
#----------------------------------------------------------------------------
rooms = {}
clients_connecting = {}


@app.route(HOMEPAGE_ROUTE)
def homepage(var=random.randint(0, 1000)):
    """
    The function returns the homepage html template.
    """
    return render_template("index.html", var=var)

#----------------------------------------------------------------------------
app.config['UPLOAD_FOLDER'] = "files"
# config
app.config.update(DEBUG=True, SECRET_KEY=SECRET_KEY)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
#-----------------------------------SocketIO Update function-----------------------------------------


@socket.on(UPDATE_ROUTE)
def update(update_data):
    """
    The function receives file updates from one user, and sends the update to
    all the users that are working on the same file.
    """
    #need to delete the print line
    print update_data
    emit(UPDATE_ACTION, update_data, broadcast=True, include_self=False)
    text_file = open(FILES_PATH+session[WORKING_FILE], WRITE_ACTION)
    text_file.write(update_data)
    text_file.close()
    return OK

#--------------------------------LOGIN AND LOGOUT--------------------------------


@app.route(LOGIN_ROUTE, methods=[METHOD_GET, METHOD_POST])
def login(var=random.randint(0, 1000), error=None):
    """
    The function can get a POST or GET requests.
    if the request is GET: returns the html login_page template
    if the request is POST: checks the data(email and password) in the users database.
    """
    global clients_connecting
    if request.method == METHOD_POST:
        email = request.form[EMAIL]
        password = request.form[PASSWORD]
        if data_base.authenticate(email, password):
            print "yesss"
            user = data_base.get_user_by_email(email)
            session[USER_ID] = user.get_id()
            session[USER_NAMESPACE] = data_base.get_username_by_id(user.get_id())+"-"+user.get_id()
            print request.remote_addr
            print clients_connecting
            if email in clients_connecting.keys() and clients_connecting[email] == request.remote_addr:
                login_user(user)
                del clients_connecting[email]
                print clients_connecting
                email = ""
                return redirect(HOMEPAGE_ROUTE)
            else:
                return render_template(LOGIN_PAGE_PATH, error=ERROR_MSG)
        else:
            return render_template(LOGIN_PAGE_PATH, error=ERROR_MSG)
    else:
        return render_template(LOGIN_PAGE_PATH, var=var, error=error)


@app.route(LOGOUT_ROUTE)
@login_required
def logout(var=random.randint(0, 1000)):
    """
    The function end the session with a user.
    and returns the login_page html template with a logged out error.
    """
    session.pop(USER_ID)
    logout_user()
    return render_template(LOGIN_PAGE_PATH, var=var, error=ERROR_MSG_LOGOUT)


@app.route(REGISTER_ROUTE, methods=[METHOD_POST])
def register(var=random.randint(0, 1000)):
    error = ""
    name = request.form['fname'] + " " + request.form['lname']
    email = request.form[EMAIL]
    password = request.form[PASSWORD]
    if not data_base.check_email(email):
        error = ERROR_MSG_ALREADY_USED
    else:
        new_user = User(name, password, email, generate_user_id())
        data_base.insert_user(new_user)
        login_user(new_user)
        return files()
    return render_template(LOGIN_PAGE_PATH, var=var, error=error)


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    #need to change !
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(id):
    return data_base.get_user_by_id(id)

#--------------------------------FILES AND EDITOR-------------------------------------------


@app.route('/download', methods=['GET', 'POST'])
def download():
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print uploads
    user_file_name = request.args.get("file_name")
    file_name = data_base_files.user_to_server_file_name_owned(user_file_name, session[USER_ID])[0]
    if not file_name:
        file_name = data_base_files.user_to_server_file_name_not_owned(user_file_name, session[USER_ID])[0]
    if file_name:
        data_base_files.html_to_word(file_name, user_file_name)
        new_file_name = user_file_name.split(".")[0]+".docx"
        print new_file_name
        return send_from_directory(directory=uploads, filename=new_file_name)
    else:
        return ERROR_404


@socket.on(CREATE_FILE)
def create_file(file_name):
    if not file_name in data_base_files.get_user_files_list(session[USER_ID]):
        data_base_files.insert_file(session[USER_ID], file_name)
        socket.emit('file_created', get_new_file_html_template(file_name), room=session[USER_NAMESPACE])
    else:
        socket.emit(POPUP_MSG, ALREADY_USED)
    return OK


def get_new_file_html_template(file_name):
    return HTML_FILE_TEMPLATE.replace("%s", file_name)


@app.route(GET_IMAGE_ROUTE)
def get_image(image_name=None):
    """
    Returns the requested image
    """
    return send_file(image_name, mimetype='image')


@app.route(TEXT_EDITOR_ROUTE)
@login_required
def text_editor(data="", var=random.randint(0, 1000)):
    """
    Returns the text editor template with the data it already has from the server.
    """
    return render_template(TEXT_EDITOR_PATH, data=data, var=var)


@app.route(FILE_REQUEST_ROUTE)
@login_required
def file_request(file_name=None):
    session[WORKING_FILE] = user_to_server_file_name(file_name)
    data_from_file = open(FILES_PATH+session[WORKING_FILE], READ_B_ACTION).read()
    return text_editor(data=data_from_file)


@app.route('/upload', methods=[METHOD_GET, METHOD_POST])
def upload():
    #not tested
    if request.method == METHOD_POST:
        file_name = request.form['file_name']
        f = request.files['the_file']
        f.save('files/%s'), file_name


def user_to_server_file_name(user_file_name):
    """
    The function returns the real name of the file by the user file name and his id
    """
    server_file_name = data_base_files.user_to_server_file_name_owned(user_file_name, session["user_id"])
    if server_file_name:
        return server_file_name[0]
    else:
        return data_base_files.user_to_server_file_name_not_owned(user_file_name, session["user_id"])[0]


def generate_user_id():
    return max([int(x[0]) for x in data_base.get_users_id()])+1


@app.route(FILES_ROUTE)
@login_required
def files(var=random.randint(0, 1000)):
    """
    The function returns the html template with the files the user has permission to
    or owned by him.
    """
    files_list = data_base_files.get_user_files_list(session[USER_ID])
    return render_template(FILES_VIEW_PATH, var=var, files_list=files_list)


@socket.on('Delete')
def delete_file(file_name):
    msg = DELETED % file_name
    data_base_files.delete_file(user_to_server_file_name(file_name), session[USER_ID])
    socket.emit('file-deleted', file_name)
    socket.emit(POPUP_MSG, msg, room=session[USER_NAMESPACE])
    return OK


@socket.on('joined')
def joined():
    room = session[USER_NAMESPACE]
    join_room(room)


@socket.on('leave')
def on_leave():
    leave_room(session[USER_NAMESPACE])


@app.route("/login_key", methods=['POST', 'GET'])
def login_key():
    user_email = request.data
    print user_email
    password_key = data_base.get_key_by_email(user_email)
    return password_key


@app.route('/secret_password', methods=['POST', 'GET'])
def secret_password():
    global clients_connecting
    params = request.data.split(" ")
    print params
    if data_base.check_authentication(params[0], params[1]): #email + second_pass
        clients_connecting[params[0]] = request.remote_addr
    return data_base.change_key(params[0])


if __name__ == "__main__":
    key = os.path.dirname(os.path.abspath(__file__))+'/static/key.pem'
    cert = os.path.dirname(os.path.abspath(__file__))+'/static/cert.pem'
    socket.run(app, host="0.0.0.0", debug=True, keyfile=key, certfile=cert)





