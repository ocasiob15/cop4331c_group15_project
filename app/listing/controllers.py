import os

from flask import Blueprint, request, render_template, \
                  flash, g, session, Response, redirect, url_for, jsonify

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval     import IntervalTrigger

import atexit

import json

from app import app, db, mail

from flask_mail import Message

# local modules
from app.listing import forms
from app.listing.models import Listing
from app.listing.forms  import CreateListingForm, UpdateListingForm,\
                               ListingSearchForm, DeleteListingForm,\
                               PlaceBidForm

# needs the User model to perform joins
from app.user.models import User

from app.file.controllers import upload_images

from datetime import datetime

from sqlalchemy import or_, and_
from sqlalchemy.sql.expression import func

listing = Blueprint('listing', __name__)

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

    form = PlaceBidForm(request.form) if listing.type == "auction" else None

    if form is not None:
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

        if form.end.data < form.start.data:
            form.errors["end"] = ["End date must be after start date"]

        elif form.validate_on_submit():

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

    # search parameters with defaults
    seller_id  = request.args.get('seller_id') or None
    sort_by    = request.args.get('sort_by')   or 'start'
    sort_ord   = request.args.get('sort_ord')  or 'asc'
    status     = request.args.get('status')    or None
    keyword    = request.args.get('keyword')   or None
    limit      = request.args.get('limit')     or None

    # removed this as start and end date facets seemed complicated and not widely used
    #.filter(and_(or_(start is None, type(start) is str and Listing.start >= start), or_(end is None, type(end) is str and Listing.start <= end)))\

    # perform a series of filters. if parameter is not passed, treat it as 'dont' care
    listings = db.session.query(Listing)\
        .filter(or_(Listing.seller_id == seller_id, seller_id is None))\
        .filter(or_(keyword is None, type(keyword) == str and Listing.title.like("%"+keyword+"%")))\
        .filter(or_(status is None, type(status) == str and status == Listing.status))\
        .order_by(getattr(getattr(Listing, sort_by), sort_ord)())\
        .limit(limit)\
        .all()

    result = [ listing.to_dict() for listing in listings]

    return jsonify(result)

"""
# REMOVED - decided to deprecate bid model
# loads all bids on a listing
@listing.route("/listing/<int:id>/bids", methods=["GET"])
def listing_bids(id):

    # get last 10 bids
    bids = db.session.query(Bid).filter(Bid.listing_id == id)\
        .order_by(Bid.date.desc())\
        .limit(10)

    result = [bid.to_dict() for bid in bids]

    return jsonify(result)

"""

# will increase the 'ask' on an 'auction' type listing and update
# the 'winner' id field of that listing
@listing.route("/listing/<int:listing_id>/place-bid", methods=["POST"])
def place_bid(listing_id):

    user = session['user'] if 'user' in session else None

    if not user:
        return

    form = PlaceBidForm(request.form)

    if not form.validate_on_submit():
        return jsonify({
            "success": False,
            "errors": form.errors
        })

    listing = db.session.query(Listing).get(listing_id)

    inactive    = listing.status != "active"
    non_auction = listing.type   != "auction"

    # prevent bids on non-active, auction listings
    if listing is None or inactive or non_auction:
      return jsonify({
          "success": False,
          "errors": {"offer" : ["Bid must be placed on an active, auction style listing"]}
      })

    offer = form.offer.data

    if offer < listing.ask:
      return jsonify({
          "success": False,
          "errors": {"offer": ["You must bid at least the current asking price or higher"]}
      })

    """
    # REMOVED - decided to deprecate bid model
    # check if bid exists
    current_bid = db.session.query(Bid)\
        .filter(and_(Bid.user_id == user['id'], Bid.listing_id == listing_id)).first()

    # if there is a bid for this user
    if current_bid is not None:
        # perform an UPDATE on listing's ask and current bid
        current_bid.offer = offer
        current_bid.date  = datetime.now()
        listing.ask       = offer
        db.session.commit()
        return jsonify({ "success" : True})

    form.user_id.data = user['id']

    # insert new bid
    bid = Bid(user['id'], listing_id, form.offer.data)

    db.session.add(bid)

    """

    # get last winner id
    winner = listing.winner

    # if last winner is not None and that new winner is not current, send them an e-mail
    if winner is not None and user['id'] != winner:

        # get winner before they are replaced
        last_winner = db.session.query(User).get(winner)

        # take their email
        email = last_winner.email

        mail_body = render_template('mail/lost_place.html', listing=listing)

        msg = Message(
            "You've Lost Your Place!",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email],
            html=mail_body
        )

        mail.send(msg)

    # set new winner
    listing.winner = user['id']

    # update asking price
    listing.ask = offer

    db.session.commit()

    return jsonify({"success": True, "new_ask": float(offer)})

def poll_listings():

    # current time
    now = datetime.now()

    print ("polling listing status at %s:" % (now))

    # look for listings that have just started
    active_listings = db.session.query(Listing)\
        .filter(Listing.status == "not_started")\
        .filter(and_(Listing.start <= now, Listing.end > now)).all()

    for active_listing in active_listings:
        # mark them as started
        active_listing.status = "active"

    print("%s have started" % len(active_listings))

    # get all listings that have ended
    ended_listings = db.session.query(Listing)\
        .filter(Listing.status == "active")\
        .filter(Listing.end <= now).all()

    # go get the winner from the bids
    for ended_listing in ended_listings:

        # mark listing as ended. Ended listing cannot be bid on.
        # if it is 'buy-now', it cannot be bought either
        ended_listing.status = "ended"

        # exit early if not an auction. send email to winner
        if ended_listing.type != "auction":
            continue

        """
        # REMOVED - deprecated the bid model
        # look for winning bid
        winning_bid = db.session.query(Bid.user_id)\
                         .filter(Bid.listing_id == ended_listing.id)\
                         .group_by(Bid.user_id)\
                         .order_by(Bid.offer.desc()).first()

        winner = winning_bid.user_id if winning_bid is not None else None

        # set the listings winner to the bid's user id. (can be no winner, or None)
        ended_listing.winner = winner

        """

        winner = ended_listing.winner

        # if there's no winner, don't send an e-mail
        if winner is None:
            break

        # send the winner an e-mail
        mail_body = render_template("mail/winner.html", listing=ended_listing)

        # get user e-mail
        winning_user = db.session.query(User).get(winner)
        email = winning_user.email

        # build message
        msg = Message(
            "You've Won!",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email],
            html=mail_body
        )

        # send it
        mail.send(msg)

    print("%s have ended" % len(ended_listings))

    # mark ended listings as ended

    # save changes
    db.session.commit()


# TODO: there is a bug with 'debug' mode in flask, which will
# cause APscheduler to schedule jobs twice. I took a moment to
# see work-arounds, but they seemed to affect auto-reload (a nice
# development feature). if a better work-around is found, put it in place

# run this task every minute
scheduler = BackgroundScheduler()

scheduler.start()

scheduler.add_job(
    func=poll_listings,
    trigger=IntervalTrigger(minutes=1),
    id="poll_listings",
    name="Poll listings for statuses and auction winners",
    replace_existing=True)

# register the anonymous function
atexit.register(lambda: scheduler.shutdown())

# allow a user to revoke their bid before the auction is over
@listing.route("/listing/<int:id>/revoke-bid")
def revoke_bid(id):
    pass

# pay for an item. allows payment if the listing is 'buy-it-now' style or
# if it is an auction and the requesting user has won.
@listing.route("/listing/<int:id>/payment")
def make_payment(id):
    pass
