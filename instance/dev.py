import os, secrets

AUCTION_SITE_TITLE = "Auction Website"

AUCTION_SITE_ROOT = "http://localhost:8000"

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/.."

# SQL alchemy configs
SQLALCHEMY_TRACK_MODIFICATIONS = False

# configured to use root with no password on localhost
SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost:3360/group_15_project"

# paypal api
PAYPAL_EMAIL  = "cop4331cgroup15test@gmail.com"
PAYPAL_PW     = "Fifteen-testS15"
PAYPAL_KEY    = ""
PAYPAL_SECRET = ""

# coinbase api
COINBASE_KEY    = ""
COINBASE_SECRET = ""

# mail settings
MAIL_SERVER   = "smtp.gmail.com"
MAIL_PORT     = 465
MAIL_USE_SSL  = True
MAIL_USERNAME = "cop4331cgroup15test@gmail.com"
MAIL_PASSWORD = "aA@12345"

# users can only upload images for now. '/img'
# portion is still decided by the function call on upload
UPLOAD_DIR = BASE_DIR + "/app/static"
EXTENSION_WHITELIST = set(['jpg', 'jpeg', 'png'])
MAX_CONTENT_SIZE = 15 * 1024 * 1024

# turn off caching to prevent static resources from being cached
CACHE_TYPE = None


DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True

SECRET_KEY = secrets.token_urlsafe(64)

# TRAP_HTTP_EXCEPTIONS = True
