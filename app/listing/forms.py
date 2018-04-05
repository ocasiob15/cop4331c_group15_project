from flask_wtf import Form

from wtforms import TextField, HiddenField, BooleanField, SelectField, \
                    DecimalField, SubmitField, FileField

from wtforms.widgets import TextArea

import wtforms.fields.html5 as html5

from wtforms.validators import Required, Length, Regexp, Optional
from wtforms_components import DateRange
from flask_wtf.file import FileRequired

from app.customized.wtforms import MultipleFileInput, field_to_title, field_to_lower

from datetime import date, datetime

class CreateListingForm(Form):

  title = TextField('Title', [Required()], filters=[field_to_title], description="listing title")

  images = FileField('Upload', [FileRequired()], widget=MultipleFileInput(), description="listing images")

  description = TextField('Description', [Required()], widget=TextArea(), description="description")

  bitcoin = BooleanField('Accept Bitcoin', [Optional()], description="accept bitcoin")

  type = SelectField('Listing Style',
      [Required()],
      choices=[('auction', 'Auction Style'),('buy_now', 'Buy It Now')],
      description="style of listing")

  ask = DecimalField('Minimum Bid', [Required()], description="asking price")

  start = html5.DateField('Start Date', [
    Required(),
    DateRange(min=date.today())
    ], description="listing start date")

  end = html5.DateField('Good Until', [
    Required(),
    DateRange(min=date.today())
    ], description="listing end date")

  submit = SubmitField("Create")

class ListingSearchForm(Form):

  keyword = TextField('Search Keyword', [], description="search keyword. e.g. shoes")

  sort_by  = SelectField('Sort By', [Required()], choices=[('start', 'Date'), ('ask', 'Price')])

  sort_ord = SelectField('Sort Ord.', [Required()], choices=[('asc', 'Asc'), ('desc', 'Desc')])

  tag = TextField('Tags', [], description="tags. separate by comma")

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
