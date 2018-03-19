from flask_wtf import Form

from wtforms import SubmitField, HiddenField, TextField, BooleanField, FormField

import wtforms.fields.html5 as html5

class BillingInformation(Form):

    billing_street = TextField('Street')
    billing_city   = TextField('City')
    billing_state  = TextField('State')
    billing_zip    = TextField('Zip Code')

class ShippingInformation(Form):

    same_as_billing = BooleanField('Same As Billing')

    shipping_street = TextField('Street')
    shipping_city   = TextField('City')
    shipping_state  = TextField('State')
    shipping_zip    = TextField('Zip Code')


class CreatePaymentForm(Form):

    # listing id,
    listing_id = HiddenField('Listing ID')

    billing_information = FormField(BillingInformation)
    shipping_information = FormField(ShippingInformation)

class CreatePaypalPaymentForm(CreatePaymentForm):

    paypal_email = html5.EmailField('PayPal E-mail')

    submit = SubmitField('Pay Now')

class CreateBitcoinPaymentForm(CreatePaymentForm):

    wallet_address = TextField('BitCoin Wallet Address')

    submit = SubmitField('Pay Now')

