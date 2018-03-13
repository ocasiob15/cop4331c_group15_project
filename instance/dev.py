import os, secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = False

AUCTION_SITE_TITLE = "Auction Website"

# configured to use root with no password on localhost
SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost:3360/group_15_project"

# turn off caching to prevent static resources from being cached
CACHE_TYPE = None

AUCTION_SITE_ROOT = "http://localhost:8000"

MAIL_SERVER   = "smtp.gmail.com"
MAIL_PORT     = 465
MAIL_USE_SSL  = True
MAIL_USERNAME = "cop4331cgroup15test@gmail.com"
MAIL_PASSWORD = "aA@12345"

DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True

SECRET_KEY = secrets.token_urlsafe(64)

# TRAP_HTTP_EXCEPTIONS = True
