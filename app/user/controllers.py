from flask import Blueprint, request, session, jsonify,\
                  url_for, redirect, render_template

from app import db
from app.user.models import User

user = Blueprint('user', __name__)

# small discrepency in language here. when viewing another person's profile
# the url usually describes a profile (something that's viewed publicly)
# whereas an 'account' usually describes one's own resource which can be
# viewed, edited or removed
@user.route('/account/')
def account ():
    user = session['user'] if 'user' in session else None
    if user is None:
        return redirect(url_for('auth.login'))
    else:
        #proxies the 'view' function below
        return view(user['id'])

@user.route('/account/<int:id>/edit')
def edit (id):
  user = db.session.query(User).get(id)
  return render_template('user/edit.html', viewed_user=user)

@user.route('/account/<int:id>/delete')
def delete (id):
  user = db.session.query(User).get(id)
  return render_template('user/delete.html', viewed_user=user)

# View other user profile. nothing stops a user from passing in their
# own ID, as these are essentially the same
@user.route('/profile/<int:id>')
def view (id):
  user = db.session.query(User).get(id)
  return render_template('user/view.html', viewed_user=user)
