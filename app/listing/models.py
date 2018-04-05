from app import app, db
from app.customized.sqlalchemy import sqla_todict

# use mysql dialect for Int to allow display width and unsigned
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.hybrid import hybrid_property

from datetime import datetime

class Listing(db.Model):

    __tablename__ = "listing"

    id = db.Column('id',
                   INTEGER(display_width=10, unsigned=True),
                   primary_key=True,
                   autoincrement=True)

    title = db.Column('title', db.VARCHAR(60), nullable=False)

    description = db.Column('description', db.VARCHAR(255), nullable=False)

    seller_id = db.Column(
        'seller_id',
        INTEGER(display_width=10, unsigned=True),
        db.ForeignKey('user.id')
    )

    type = db.Column('type', db.VARCHAR(45), default="auction", nullable=False)

    # includes [active, not_started, sold]
    status = db.Column('status', db.VARCHAR(45), default="active", nullable=False)

    date_created = db.Column('date_created', db.DATETIME, nullable=False, default=datetime.now)

    # start and end date. duration calculated functionally
    start = db.Column('start', db.DATETIME, nullable=False)
    end   = db.Column('end', db.DATETIME, nullable=False)

    # is it a bitcoin style auction, 1 = yes, 0 = no.
    bitcoin = db.Column('bitcoin', INTEGER(display_width=1, unsigned=True), nullable=False, default=0)

    # asking price. functions as minimum bid, OR price of buy-it-now
    ask = db.Column('ask', db.DECIMAL(15, 8), nullable=False, default=0)

    # user id of leading bid. effectively winning bid when auction ends
    winner = db.Column(
        'winner',
        INTEGER(display_width=10, unsigned=True),
        db.ForeignKey('user.id'),
        nullable=True
    )

    # id is set via session variable (and not form data)
    def __init__ (self, seller_id):

        self.seller_id = seller_id

    def to_dict(self):
      return sqla_todict(self)

"""
# bids are modeled here because the bid behaves moreso like a relationship table
# "user bids on a listing". Routes will also heavily rely on listing id.
class Bid(db.Model):

    __tablename__ = "bid"

    # both user_id and listing_id make a composite primary key, after all, each user may
    # only place a single bid on each item
    user_id = db.Column(
        'user_id',
        INTEGER(display_width=10, unsigned=True),
        db.ForeignKey('user.id'),
        primary_key=True
    )

    listing_id = db.Column(
        'listing_id',
        INTEGER(display_width=10, unsigned=True),
        db.ForeignKey('listing.id'),
        primary_key=True
    )

    date  = db.Column('date', db.DATETIME, nullable=False, default=datetime.now)

    offer = db.Column('offer', db.DECIMAL(15, 8), nullable=False)

    def __init__(self, user_id, listing_id, offer):
        self.user_id    = user_id
        self.listing_id = listing_id
        self.offer      = offer

    def to_dict(self):
        return sqla_todict(self)
"""
