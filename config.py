import os, secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

from sys import argv

env = argv[1] if len(argv) > 1 else "dev"

SQLALCHEMY_TRACK_MODIFICATIONS = False

if env == "dev":
    # configured to use root with no password on localhost
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost:3360/group_15_project"

    # turn off caching to prevent static resources from being cached
    CACHE_TYPE = None

elif env == "prod":
    # just change this to whatever in your production environment
    SQLALCHEMY_DATABASE_URI = "mysql://someuser:somepassword@localhost:3360/group_15_project"


DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True

CSRF_SESSION_KEY = secrets.token_urlsafe(64)

SECRET_KEY = secrets.token_urlsafe(64)

TRAP_HTTP_EXCEPTIONS = True
