from flask_wtf import Form

from wtforms import TextField, PasswordField, SubmitField

import wtforms.fields.html5 as html5

from wtforms.validators import Required, Regexp, Length, Email, EqualTo

class LoginForm(Form):
    credentials = TextField('Username or Email', [
        Required(message="Please enter your username or email")
        ])

    password = PasswordField('Password', [
        Required(message="Please enter your password")
        ])

    submit = SubmitField("Log In")

class SignupForm(Form):

    first_name = TextField('First Name', [
        Required(message="You must provide your first name"),
        Length(min=1, max=45, message="First name must be between 1 and 45 characters")
        ])

    last_name = TextField('Last Name', [
        Required(message="You must provide your last name"),
        Length(min=1, max=45, message="Last name must be between 1 and 45 characters")
        ])

    username = TextField('Username', [
        Required(message="You must provide a username"),
        Length(min=1, max=45, message="Username must be between 1 and 45 characters")
        ])

    email = html5.EmailField('Email', [
        Required(message="You must provide an email address"),
        Length(min=1, max=60, message="Email must be between 1 and 60 characters")
        ])

    password_regexp_message  = "Your password must meet the character requirements: 1 lowercase,"
    password_regexp_message += "1 uppercase, 1 number, 1 special character ($, #, @, !)"

    password = PasswordField('Password', [
        Required(message="You must provide a password"),
        Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])",
          message=password_regexp_message),
        Length(min=8, message="Your password must be at least 8 characters long")
        ])

    submit = SubmitField('Sign Up')

