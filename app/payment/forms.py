from flask_wtf import Form

from wtforms import SubmitField, HiddenField, TextField, BooleanField, FormField

from wtforms.validators import Required, Length, Regexp

import wtforms.fields.html5 as html5

class CreatePaymentForm(Form):

    # listing id,
    listing_id = HiddenField('Listing ID')

    incomplete_bill_msg = "Please complete your billing address"

    billing_street = TextField('Street', [Required(incomplete_bill_msg)])
    billing_city   = TextField('City', [Required(incomplete_bill_msg)])
    billing_state  = TextField('State', [Required(incomplete_bill_msg)])
    billing_zip    = TextField('Zip Code', [Required(incomplete_bill_msg)])

    same_as_billing = BooleanField('Same As Billing')

    incomplete_ship_msg = "Please complete your shipping address"

    shipping_street = TextField('Street', [Required(incomplete_ship_msg)])
    shipping_city   = TextField('City', [Required(incomplete_ship_msg)])
    shipping_state  = TextField('State', [Required(incomplete_ship_msg)])
    shipping_zip    = TextField('Zip Code', [Required(incomplete_ship_msg)])


class CreatePaypalPaymentForm(CreatePaymentForm):

    # credit card regex is super minimal. just checks for decimal between 13 and 16 characters
    # TODO: validate if it is Visa, Mastercard and so on
    credit_card = TextField('Credit Card Number', [
        Required("Please enter your credit card number"),
        Regexp(r"^[0-9]{13,16}$", message="Please Enter a valid credit card number")])

    exp_date = TextField('Expiration Date', [
      Required("Please enter your card expiration date (e.g. mm/yy)"),
      Regexp(r"^(1[1-2]|0[1-9])\/[0-9]{2}$", message="Please enter a valid expiration date")])

    cvv = TextField('CVV', [
      Required("Please enter the CVV on your credit card"),
      Regexp(r"^[0-9]{3,4}$", message="Please enter a valid CVV")])

    submit = SubmitField('Pay Now')

class CreateBitcoinPaymentForm(CreatePaymentForm):

    wallet_address = TextField('BitCoin Wallet Address', [Required("Please enter a Bitcoin wallet address")])

    submit = SubmitField('Pay Now')

