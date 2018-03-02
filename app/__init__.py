from flask import Flask, flash, request, session, render_template,\
                  send_from_directory, jsonify, redirect, url_for

from werkzeug.exceptions import HTTPException

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# use configuration from config.py
app.config.from_object('config')

# allow matching of URLs with or without trailing '/'
app.url_map.strict_slashes = False

# initialize database using the app and its settings
db = SQLAlchemy(app)

# route error handling
def default_handler(error):

    code = error.code if isinstance(error,HTTPException) else 500

    if code >= 500:
        # show special message on 500 errors
        return render_template('50x.html'), 500
    else:
        # return 404 for other status codes (even 30x)
        return render_template('404.html'), 404

#register the handler for 404
app.register_error_handler(404, default_handler)
# TODO: conditionally handle 500 errors. taken out of dev environment
# because it was making it tricky to debug
# register the handler for 50
# app.register_error_handler(500, default_handler)
# register the handler for any exception (should not handle if in debug mode)
# app.register_error_handler(Exception, default_handler)

# module controllers
from app.auth.controllers    import auth    as auth_controller
from app.user.controllers    import user    as user_controller
from app.listing.controllers import listing as listing_controller
# and so on...

app.register_blueprint(auth_controller)
app.register_blueprint(listing_controller)
app.register_blueprint(user_controller)
# see auth module for example. user model started, please adjust
# register(user_controller)
# register(listing_controller)
# and so on...

# had some serious trouble with getting flash messages to show up.
# researched how to have variables accessible to all templates (instead
# of passing each time for every route). preferred way is a context_processor
@app.context_processor
def template_vars():
  user = session['user'] if 'user' in session else None
  return dict(user=user)

# paths for entity agnostic pages (home page, contact, about, whatever)
@app.route('/')
def home():
    return render_template("index.html", page_title="Crypto Auctions")

@app.route('/about/')
def about():
    return render_template("about.html", page_title="About Us")

# paths for static resources (js, css, images)
# user requested js
@app.route('/js/<path:path>')
def send_script(path):
    return send_from_directory('static/js', path)

# user requested css
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/style/css', path)

# user requested images
@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

# commenting this out until we can get basic site functionality rolling
db.create_all()
