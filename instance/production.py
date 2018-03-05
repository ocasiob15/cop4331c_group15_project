import os, secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = False

AUCTION_SITE_TITLE = "Auction Website"

# just change this to whatever in your production environment
SQLALCHEMY_DATABASE_URI = "mysql://someuser:somepassword@localhost:3360/group_15_project"

AUCTION_SITE_ROOT = "[put some domain here for site root url]"

MAIL_SERVER   = "mail.somedomain.com"
MAIL_PORT     = "465"
MAIL_USE_TLS  = False
MAIL_USE_SSL  = True
MAIL_USERNAME = "someuser@somedomain.com"
MAIL_PASSWORD = "somepassword"

DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True

SECRET_KEY = secrets.token_urlsafe(64)

# TRAP_HTTP_EXCEPTIONS = True
