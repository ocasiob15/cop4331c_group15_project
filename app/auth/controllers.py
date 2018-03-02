from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

import bcrypt

from app import db


from app.auth.forms import LoginForm, SignupForm

from app.user.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET', 'POST'])
def login():

    form = LoginForm(request.form)


    if form.validate_on_submit():
        pass
        #user = User.query.filter_by().first()

    return render_template("auth/login.html", page_title="Log In", form=form)

@auth.route('/signup/', methods=["GET", "POST"])
def signup():

    form = SignupForm(request.form)

    if form.validate_on_submit():
        pass

    return render_template("auth/signup.html", page_title="Sign Up", form=form)

