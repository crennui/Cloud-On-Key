__author__ = 'Tamir'
import random
from flask import flash
from flask import request
from flask import abort
from flask import redirect
from flask import Flask
from flask import send_file
from flask import render_template
from flask import request
from flask_Login import *
from flask_wtf import *
from wtforms import *
from flask import url_for
#LoginManager, UserMixin, login_required

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
login_manager = LoginManager()
login_manager.init_app(app)


@app.route(HOMEPAGE_ROUTE)
@app.route(USER_ROUTE)
def homepage(user=None, var=random.randint(0, 1000)):
    return render_template("index.html", user=user, var=var)

#----------------------------------------------------------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)
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



