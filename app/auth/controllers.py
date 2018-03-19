from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify

import bcrypt, secrets

from app import db, mail

from flask_mail import Message

from app.auth.forms  import LoginForm, SignupForm
from app.auth.models import UserAuthentication
from app.user.models import User

from sqlalchemy import or_

auth = Blueprint('auth', __name__)

from flask import current_app as app

@auth.route('/login/', methods=['GET', 'POST'])
def login():

    form = LoginForm(request.form)

    if form.validate_on_submit():

        credentials = form.credentials.data
        password    = form.password.data

        # get user by username or email
        user = db.session.query(User).filter(
            or_(User.username == credentials, User.email == credentials)
        ).first()

        if (user.blocked == 1):
            error = "This account is unable to log in. "
            error += "Make sure it is authenticated, or has not been blocked."
            form.errors['unauthorized'] = error

        elif (user is not None and bcrypt.checkpw(password, user.hash)):
            session['user'] = {"id": user.id, "username": user.username, "admin": user.admin}
            return redirect(url_for('user.account'))
        else:
            form.errors['credentials'] = "Invalid credentials or password"

    return render_template("auth/login.html", page_title="Log In", form=form)

@auth.route('/signup/', methods=["GET", "POST"])
def signup():

    form = SignupForm(request.form)

    if form.validate_on_submit():

        # get data from form
        password = form.password.data

        # hash user password
        pwhash = bcrypt.hashpw(password, bcrypt.gensalt(12))

        email = form.email.data

        # insert into DB
        user = User(form.first_name.data,
                    form.last_name.data,
                    form.username.data,
                    email,
                    pwhash)

        # generate one time auth token
        auth_token = secrets.token_urlsafe(64)

        # insert user into DB
        db.session.add(user)
        db.session.commit()

        # create the pair of user id and auth token
        user_authentication = UserAuthentication(user.id, auth_token)

        # put the auth token in the DB
        db.session.add(user_authentication)
        db.session.commit()

        # get welcome/authentication email
        welcome_body = render_template("mail/welcome.html", auth_token=auth_token)

        # build message
        msg = Message(
            "Welcom to the Auction Site",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email],
            html=welcome_body
        )

        # send it
        mail.send(msg)

        # set flash message in the session
        flashmsg = ("Thank you for creating your account, "
                    "to begin using it, you will have to authenticate it "
                    "using the email we have sent")

        flash(flashmsg)

        # redirect to home page
        return render_template("index.html")

    return render_template("auth/signup.html", page_title="Sign Up", form=form)

@auth.route('/logout/', methods=["GET"])
def logout():
    del session['user']
    return redirect(url_for("home"))

@auth.route('/authenticate/<string:auth_token>', methods=["GET"])
def authenticate(auth_token):

    # TODO: get token from params, query db for existing token,
    auth = db.session.query(UserAuthentication).get(auth_token)

    # return if there is no auth_token
    if not auth:
      return

    # if there is a match, update user record to be able to log in
    user_id = auth.user_id

    # get user using the id
    user = db.session.query(User).get(user_id)

    # return if there is no user
    if not user:
      return

    # remove record of auth_token
    db.session.delete(auth)

    # update user record to not be blocked
    user.blocked = 0

    db.session.commit()

    flashmsg = ("Thanks for verifying your account. you may now log in"
                " and begin using the Auction Website")

    flash(flashmsg)

    # if there's no match, die
    return redirect(url_for("auth.login"))
