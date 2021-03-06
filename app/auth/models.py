from app import db

from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.schema import ForeignKey

class UserAuthentication(db.Model):

  __tablename__ = "user_authentication"

  auth_token = db.Column(db.VARCHAR(86), nullable=False, primary_key=True)

  user_id = db.Column(INTEGER(display_width=10, unsigned=True),
                      ForeignKey("user.id"),
                      unique=True)

  def __init__ (self, user_id, auth_token):
    self.user_id    = user_id
    self.auth_token = auth_token
