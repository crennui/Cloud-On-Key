__author__ = 'Tamir'
import random
from flask import Flask
from flask import send_file, render_template, request, url_for, Response, redirect, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, login_url
from User import *
OK = "OK - 200"
UPDATE_ROUTE = "/update"
TEXT_EDITOR_ROUTE = "/text_editor"
USER_ROUTE = "/<user>"
HOMEPAGE_ROUTE = "/"
FILES_ROUTE = "/files"
TEXT_EDITOR_PATH = "text_editor_v2.0.html"
SHADOW_FILE_PATH = "shadow.txt"
METHOD_POST = "POST"
STATIC_PATH = "/static/"

app = Flask(__name__)


@app.route(HOMEPAGE_ROUTE)
@login_required
def homepage(user=None, var=random.randint(0, 1000)):
    return render_template("index.html", user=user, var=var)

#----------------------------------------------------------------------------

# config
app.config.update(
    DEBUG=False,
    SECRET_KEY='secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login(var=random.randint(0, 1000)):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return render_template("login_page.html", var=var)


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)

#----------------------------------------------------------------------------

@app.route('/get_image/<image_name>')
def get_image(image_name=None):
    return send_file(image_name, mimetype='image')


@app.route(TEXT_EDITOR_ROUTE)
def text_editor(data=None, var=random.randint(0, 1000)):
    return render_template(TEXT_EDITOR_PATH, data=data, var=var)


@app.route(UPDATE_ROUTE, methods=[METHOD_POST])
def update_shadow():
    text_file = open(SHADOW_FILE_PATH, "w")
    print request.data
    text_file.write(request.data)
    text_file.close()
    return OK


@app.route("/file_request/<file_name>")
def hundle_file_request(file_name = None):
    """<a href="http://127.0.0.1:5000/file_request/name">
                <div class="img-single">
                    <img src="document_file_icon_2.png">
                    <h3>this is a test!!!ffffffffffffffffffffffffffffffffffffffffffffffffffffff</h3>
                </div></a>"""

    return text_editor()


@app.route(FILES_ROUTE)
def files(var=random.randint(0, 1000)):
    return render_template("files_view_2.html", var=var)

if __name__ == "__main__":
    app.run(host='0.0.0.0')



