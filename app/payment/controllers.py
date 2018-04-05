from flask import Blueprint, request, render_template, \
                  flash, g, session, Response, redirect, url_for, jsonify

import json

from app import app, db, mail

from flask_mail import Message

from app.payment.square import fulfill_usd_payment, fulfill_btc_payment

from app.payment.forms import CreatePaypalPaymentForm, CreateBitcoinPaymentForm

from app.listing.models import Listing
from app.user.models import User

from datetime import datetime

from sqlalchemy import or_, and_

payment = Blueprint('payment', __name__)

@payment.route('/listing/<int:listing_id>/pay/', methods=['GET', 'POST'])
def new(listing_id):

    # get user from session
    user = session['user'] if 'user' in session else None

    # redirect to login
    if user is None:
        return redirect(url_for('auth.login'))

    # query listing
    listing = db.session.query(Listing).get(listing_id)

    # query listing seller by id.
    seller_id = listing.seller_id
    seller = db.session.query(User).get(seller_id)

    if listing.bitcoin:
        form = CreateBitcoinPaymentForm(request.form)

    else:
        form = CreatePaypalPaymentForm(request.form)

    form.listing_id.data = listing.id

    # check request method
    if request.method == "POST":

        # if listing is auction
        if listing.type == "auction":

            # redirect if user not winner (undecided until auction ends)
            if user['id'] != listing.winner:
                return redirect(url_for('home'))

        # proceed if user is winner

        # return json errors if form does not validate
        if not form.validate_on_submit():
            return jsonify({"success": False, "errors":form.errors})

        # if listing is bitcoin
        if listing.bitcoin:
            result = fulfill_btc_payment(listing.ask)

        # else (usd)
        else:
            result = fulfill_usd_payment(listing.ask)

        # success!
        if (type(result) == dict):
            errors = result['errors'] if 'errors' in result else None
        else:
            errors = getattr(result, 'errors', None)

        if not errors:

            # mark listing as sold if it isn't yet
            listing.status = "sold"

            db.session.commit()

            # set flash message
            msg = ("Thank you for completing your purchase "
                   "for %s. The seller will be notified by e-mail "
                   "and will send your item shortly.") % (listing.title)

            flash(msg)

            # get winner user record
            winner = db.session.query(User).get(user['id'])

            # send seller an e-mail with shipping info
            mail_body = render_template('mail/sold.html', listing=listing, form=form, winner=winner)

            email = Message(
              "Your Item Has Sold",
              sender=app.config['MAIL_USERNAME'],
              recipients=[seller.email],
              html=mail_body
            )

            mail.send(email)

        result['redirect'] = url_for("listing.view", listing_id=listing.id)

        return jsonify(result)

    # request is GET. render the form

    #render payment form
    return render_template('payment/new.html', page_title="Submit Payment", form=form, listing=listing)

