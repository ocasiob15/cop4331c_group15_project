from flask_wtf import Form

from wtforms import TextField, HiddenField, BooleanField, SelectField, \
                    DecimalField, SubmitField, FileField

from wtforms.widgets import TextArea

import wtforms.fields.html5 as html5

from wtforms.validators import Required, Length, Regexp, Optional
from flask_wtf.file import FileRequired

from app.customized.wtforms import MultipleFileInput

from datetime import datetime

class CreateListingForm(Form):

  title = TextField('Title', [Required()])

  images = FileField('Upload', [FileRequired()], widget=MultipleFileInput())

  description = TextField('Description', [Required()], widget=TextArea())

  bitcoin = BooleanField('Accept Bitcoin', [Optional()])

  lol = "<p>hey hey hey, this hsould be a thing</p>"

  type = SelectField('Listing Style',
      [Required()],
      choices=[('auction', 'Auction Style'),('buy_now', 'Buy It Now')])

  ask = DecimalField('Minimum Bid', [Required()])

  start = html5.DateField('Start Date', [Required()])

  end = html5.DateField('Good Until', [Required()])

  submit = SubmitField("Create")

class ListingSearchForm(Form):

  keyword = TextField('Search Keyword', [])

  start = html5.DateField('Start Date', [], default=datetime.now().strftime("%Y-%m-%d"))

  end   = html5.DateField('End Date', [])

  submit = SubmitField('Search')


class UpdateListingForm(Form):

  # making life simple and allowing only titles and descriptions
  # to be edited.
  title = TextField('Title', [])

  description = TextField('Description', [], widget=TextArea())

  submit = SubmitField("Save")


class DeleteListingForm(Form):

  user_id = HiddenField()

  confirm = SubmitField("Delete")

class PlaceBidForm(Form):

  listing_id = HiddenField()

  user_id = HiddenField()

  offer = DecimalField('Bid', [])

  submit = SubmitField('Place Bid')
