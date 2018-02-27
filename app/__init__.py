from flask import Flask, render_template, send_from_directory

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

# route error handling
def default_handler(error):
    if error.code >= 500:
        # show special message on 500 errors (not run in debug mode for flask)
        return render_template('50x.html'), error.code
    else:
        # return 404 for other status codes (even 30x)
        return render_template('404.html'), 404

#register the handler for 404
app.register_error_handler(404, default_handler)
#register the handler for any exception (should not handle if in debug mode)
app.register_error_handler(Exception, default_handler)

# module controllers
from app.auth.controllers import auth as auth_controller
# from app.user.controllers import user as user_controller
# and so on...

app.register_blueprint(auth_controller)
# see auth module for example. user model started, please adjust
# register(user_controller)
# register(listing_controller)
# and so on...

# paths for entity agnostic pages (home page, contact, about, whatever)
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about/')
def about():
    return render_template("about.html")

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
# db.create_all()
