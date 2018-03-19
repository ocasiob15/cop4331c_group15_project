from flask import Blueprint, request, render_template, \
                  flash, g, session, Response, redirect, url_for, jsonify

import json

from app import app, db

from app.listing import forms
from app.listing.models import Listing, Bid
from app.listing.forms  import CreateListingForm, UpdateListingForm,\
                               ListingSearchForm, DeleteListingForm,\
                               PlaceBidForm

from app.file.controllers import upload_images

from datetime import datetime

from sqlalchemy import or_, and_

listing = Blueprint('listing', __name__)

import os
from urllib import parse as urlparse

def listing_image_urls(listing):

    image_urls = []

    base_url = app.config['AUCTION_SITE_ROOT'] + '/img/listing/' + str(listing.id) + "/"

    image_dir = os.path.join(app.config['UPLOAD_DIR'], 'img', 'listing', str(listing.id))
    if os.path.isdir(image_dir):
        files = os.listdir(image_dir)
        for filename in files:
            image_urls.append(urlparse.urljoin(base_url, filename))

    return image_urls

@listing.route("/listing/<int:listing_id>/", methods=["GET"])
def view(listing_id):

    listing = db.session.query(Listing).get(listing_id)

    listing.image_urls = listing_image_urls(listing)

    print(listing.image_urls)

    form = PlaceBidForm(request.form) if listing.type == "auction" else None

    form.listing_id.data = listing.id

    return render_template('listing/view.html', page_title=listing.title, listing=listing, form=form);

@listing.route("/listing/new/", methods=["GET", "POST"])
def new():

    form = CreateListingForm(request.form)

    # this work?
    if request.files:
        images = request.files.getlist('images')

        # set form.images.data as first image just to keep wtforms happy
        form.images.data = images[0]

        print (images)

    user = session['user'] if 'user' in session else None

    if (not user):
        pass
        # return redirect(url_for('auth.login'))

    if request.method == "POST":

        if form.validate_on_submit():

            print("notevengetting heresofarasicantell")
            listing = Listing(user['id'])
            form.populate_obj(listing)

            # check currency, if dollars, round up to hundredth
            # ... example, imagine user enters 120.209999999. they would only
            # gather approx. 1 penny, but we should still enforce no fractions
            # of a penny. bitcoin, by comparison has the satoshi as its base.
            # our database has up to 8 decimal places which should support that
            if not listing.bitcoin:
              listing.ask = round(listing.ask, 2)

            # check dates provided
            if str(form.start.data) > str(datetime.now()):
              listing.status = "not_started"

            else:
              listing.status = "active"

            db.session.add(listing)
            db.session.commit()

            # images are put under the listings directory, so the
            # id is needed.

            # check if files were received
            images = request.files.getlist('images')

            upload_images(images, 'listing', listing.id)

            flash("Check out your new listing!")

            return redirect(url_for("listing.view", listing_id=listing.id))


    return render_template('listing/new.html', page_title="New Listing", form=form);

@listing.route("/listing/<int:id>/remove/", methods=["GET", "DELETE"])
def delete(id):

    listing = db.session.query(Listing).get(id)

    user = session['user'] if 'user' in session else None

    if not user or listing.seller_id != user["id"]:
        return redirect(url_for('home'))

    if request.method == "GET":
        form = DeleteListingForm(obj=listing)

    elif request.method == "DELETE":

        form = DeleteListingForm(request.form)

        db.session.delete(listing)
        db.session.commit()

        if not form.validate_on_submit():
            return jsonify({"success": False, "errors": form.errors})

        return jsonify({"success": True})

    return render_template('listing/delete.html', page_title="Remove Listing", form=form, listing=listing);

@listing.route("/listing/<int:id>/edit/", methods=["GET", "PUT"])
def edit(id):

    listing = db.session.query(Listing).get(id)

    listing.image_urls = listing_image_urls(listing)

    user = session['user'] if 'user' in session else None

    if not user or listing.seller_id != user["id"]:
        return redirect(url_for('home'))

    if request.method == "GET":
        form = UpdateListingForm(obj=listing)

    elif request.method == "PUT":

        form = UpdateListingForm(request.form)

        form.populate_obj(listing)

        db.session.commit()

        if not form.validate_on_submit():
            return jsonify({"success": False, "errors": form.errors})

        return jsonify({"success": True, "id": id })


    return render_template('listing/edit.html', form=form, listing=listing);

# browse renders the search page
@listing.route("/browse/", methods=["GET"])
def browse():

    form = ListingSearchForm(request.form)

    return render_template('listing/browse.html', page_title="Search Listings", form=form)

# search sends the request for lists as JSON
@listing.route("/listing/search/", methods=["GET"])
def search():

    seller_id  = request.args.get('seller_id') or None
    start      = request.args.get('start')     or datetime.now().strftime("%Y-%m-%d")
    end        = request.args.get('end')       or None
    status     = request.args.get('status')    or None
    keyword    = request.args.get('keyword')   or None
    limit      = request.args.get('limit')     or None

    # perform a series of filters. if parameter is not passed, treat it as 'dont' care
    listings = db.session.query(Listing)\
        .filter(or_(Listing.seller_id == seller_id, seller_id is None))\
        .filter(and_(Listing.start >= start, or_(end is None, type(end) is str and Listing.start <= end)))\
        .filter(or_(keyword is None, type(keyword) == str and Listing.title.like("%"+keyword+"%")))\
        .filter(or_(status is None, type(status) == str and status == Listing.status))\
        .limit(limit)\
        .all()

    result = [ listing.to_dict() for listing in listings]

    return jsonify(result)

# loads all bids on a listing
@listing.route("/listing/<int:id>/bids", methods=["GET"])
def listing_bids(id):

    # get last 10 bids
    bids = db.session.query(Bid).filter(Bid.listing_id == id).limit(10)

    result = [bid.to_dict() for bid in bids]

    return jsonify(result)


# creates a bid on a listing for a user.
# behaves like an UPSERT operation.
@listing.route("/listing/<int:listing_id>/place-bid", methods=["POST"])
def place_bid(listing_id):

    user = session['user'] if 'user' in session else None

    if not user:
        return

    listing = db.session.query(Listing).get(id)

    form = PlaceBidForm(request.form)

    offer = form.offer.data

    if offer < listing.ask:
      return jsonify({
        "success": False,
        "errors": ["You must bid at least the current asking price or higher"]
      })

    form.user_id.data = user['id']

    if not form.validate_on_submit():
        return jsonify({
          "success": False,
          "errors": ["Something went wrong placing your bid"]
        })

    # insert the bid
    bid = new

    return jsonify({"success": True})


# allow a user to revoke their bid before the auction is over
@listing.route("/listing/<int:id>/revoke-bid")
def revoke_bid(id):
    pass

# pay for an item. allows payment if the listing is 'buy-it-now' style or
# if it is an auction and the requesting user has won.
@listing.route("/listing/<int:id>/payment")
def make_payment(id):
    pass
