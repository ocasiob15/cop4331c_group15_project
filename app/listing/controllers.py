from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for


from app import db

from app.listing import forms
from app.listing.models import Listing

listing = Blueprint('listing', __name__)

@listing.route("/listing/<int:id>", methods["GET"])
def view(id):
  listing = {}
  return render_template('listing/view.html', listing=listing);


