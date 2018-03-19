from flask import Blueprint, request, render_template, \
                  flash, g, session, Response, redirect, url_for, jsonify

import json

from app import db

from app.payment import coinbase, paypal
from app.payment.forms import CreatePaypalPaymentForm, CreateBitcoinPaymentForm

from app.listing.models import Listing
from app.user.models import User

from datetime import datetime

from sqlalchemy import or_, and_

payment = Blueprint('payment', __name__)

@payment.route('/listing/<int:listing_id>/pay/', methods=['GET', 'POST'])
def new(listing_id):

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
    # is POST
        user = session['user'] if 'user' in session else None
        # get user from session

        # redirect? somehow allow guest payment?
        if user is None:
            return redirect(url_for('home'))


        # if listing is auction
        elif listing.type == "auction":
            # redirect if user not winner (undecided until auction ends)
            if user is None or user['id'] != listing.winner:
                return redirect(url_for('home'))

            # proceed if user is winner


        # if listing is bitcoin
        if listing.bitcoin:
            pass


            # ping wallet to verify? maybe not necessary

            # ping seller wallet? maybe not necessary

            # take payment information from form

            # wallet ok? fullfill payment?

        # else (usd)
        else:
            pass
            # ping api to verify? maybe not necessary

            # ping api for seller? maybe not necessary

            # take payment information from form

        # attempt payment

        # success!
            # insert record using Payment model
            # set flash message
            # redirect to (same page? home page? account?)

        # fail!
            # set error on form and refresh

    # request is GET. render the form

    #render payment form
    return render_template('payment/new.html', page_title="Submit Payment", form=form, listing=listing)

