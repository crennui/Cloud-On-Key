import random
from flask import Flask
from flask import send_file, render_template, request, url_for, Response, redirect, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, login_url
from User import *
app = Flask(__name__)


@app.route("/")
def hompage(var=random.randint(0, 1000)):
    return render_template("log.html", var=var)

if __name__ == "__main__":
    app.run(host='0.0.0.0')


