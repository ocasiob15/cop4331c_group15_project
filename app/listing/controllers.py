from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify


from app import db

from app.listing import forms
from app.listing.models import Listing

from app.listing.forms import CreateListingForm, UpdateListingForm, DeleteListingForm

listing = Blueprint('listing', __name__)

@listing.route("/listing/<int:id>/", methods=["GET"])
def view(id):
  listing = {}
  return render_template('listing/view.html', listing=listing);

@listing.route("/listing/new/", methods=["GET", "POST"])
def new():
  return render_template('listing/new.html');

@listing.route("/listing/<int:id>/remove/", methods=["GET", "DELETE"])
def delete(id):
  listing = {}
  return render_template('listing/delete.html', listing=listing);

@listing.route("/listing/<int:id>/edit/", methods=["GET", "PUT"])
def edit(id):
  listing = {}
  return render_template('listing/edit.html', listing=listing);

# browse renders the search page
@listing.route("/browse/", methods=["GET"])
def browse():
  return render_template('listing/browse.html', page_title="Search Listings")

# search sends the request for lists as JSON
@listing.route("/search/", methods=["GET"])
def search():
  # TODO: get python dictionary data of listings from DB
  listings = {}
  return jsonify(listings);
