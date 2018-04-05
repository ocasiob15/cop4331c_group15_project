from flask_wtf import Form

from wtforms import TextField, HiddenField, PasswordField, SubmitField

import wtforms.fields.html5 as html5

from wtforms.validators import Required, Regexp, Length, Email, EqualTo, Optional

from app.customized.wtforms import field_to_lower, field_to_title

class EditUserForm (Form):

    id = HiddenField("User ID")

    # many of the same fields as sign up form
    first_name = TextField('First Name', [
        Required(message="You must provide your first name"),
        Length(min=1, max=45, message="First name must be between 1 and 45 characters")
        ],
        filters=[field_to_title])

    last_name = TextField('Last Name', [
        Required(message="You must provide your last name"),
        Length(min=1, max=45, message="Last name must be between 1 and 45 characters")
        ],
        filters=[field_to_title])

    username = TextField('Username', [
        Required(message="You must provide a username"),
        Length(min=1, max=45, message="Username must be between 1 and 45 characters")
        ],
        filters=[field_to_lower])

    email = html5.EmailField('Email', [
        Required(message="You must provide an email address"),
        Length(min=1, max=60, message="Email must be between 1 and 60 characters")
        ],
        filters=[field_to_lower])

    bitcoin_wallet_address = TextField("BitCoin Wallet Address", [
        Optional(),
        Regexp(r"^$|[13][a-km-zA-HJ-NP-Z1-9]{25,34}$")
        ])

    pay_pal_email = html5.EmailField("PayPal Email Address", [
        Optional(),
        ])


    submit = SubmitField("Save")

class ChangePasswordForm (Form):

    id = HiddenField("User ID")

    password_regexp_message  = "Your password must meet the character requirements: 1 lowercase,"
    password_regexp_message += "1 uppercase, 1 number, 1 special character ($, #, @, !)"

    password = PasswordField('Password', [
        Required(message="You must provide a new password"),
        Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])",
          message=password_regexp_message),
        Length(min=8, message="Your new password must be at least 8 characters long")
        ])

    password = PasswordField('Confirm Password', [
        Required(message="You must confirm your new password"),
        Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])",
          message=password_regexp_message),
        Length(min=8, message="Your password must be at least 8 characters long")
        ])

    submit = SubmitField("Change Password")

class DeleteUserForm (Form):

    user_id = HiddenField("User ID")

    submit = SubmitField("Delete Account")

