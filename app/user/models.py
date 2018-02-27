from app import db

# use dialect for mysqls integer to allow unsigned ints, and also
# allows us to set a specific 'display width' (size) for the int
from sqlalchemy.dialects.mysql import INTEGER

class User(db.Model):

    __tablename__ = 'user'

    id         = db.Column('id',
                           INTEGER(display_width=10, unsigned=True),
                           primary_key=True,
                           autoincrement=True)

    first_name = db.Column('first_name', db.VARCHAR(45), nullable=False)
    last_name  = db.Column('last_name', db.VARCHAR(45), nullable=False)

    username   = db.Column('username',
                           db.VARCHAR(45),
                           unique=True,
                           nullable=False)

    email      = db.Column('email',
                           db.VARCHAR(60),
                           unique=True,
                           nullable=False)

    hash       = db.Column('hash', db.VARCHAR(60), nullable=False)
    role       = db.Column('role', db.VARCHAR(45))

    # 1 = blocked, 0 = unblocked
    blocked    = db.Column(INTEGER(display_width=1, unsigned=True))

    def __init__(self, first_name, last_name, username, email, hash):
        self.first_name = first_name
        self.last_name  = last_name
        self.username   = username

    def __repr__(self):
        return "%s" % (self.username)

