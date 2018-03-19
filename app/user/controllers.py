from flask import Blueprint, request, session, jsonify,\
                  url_for, redirect, render_template

from app import db
from app.user.models import User

from app.user.forms import EditUserForm, ChangePasswordForm, DeleteUserForm

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

@user.route('/account/<int:id>/edit', methods=["GET", "PUT"])
def edit (id):

    user = db.session.query(User).get(id)

    if request.method == "GET":

        form = EditUserForm(obj=user)

        return render_template('user/edit.html', form=form, viewed_user=user)


    elif request.method == "PUT":

        form = EditUserForm(request.form)

        # check if it is not valid
        if not form.validate_on_submit():
            # return JSON response of errors
            return jsonify({"success": False, "errors": form.errors})

        # form has data. set the users info
        user.first_name = form.first_name.data
        user.last_name  = form.last_name.data
        user.email      = form.email.data

        # user.bitcoin_wallet_address = form.bitcoin_wallet_address.data

        # save record
        db.session.commit()

        # send JSON response indicating success
        return jsonify({"user_id": id, "success": True})

@user.route('/account/<int:id>/delete', methods=["GET", "DELETE"])
def delete (id):

    user = session['user'] if 'user' in session else None

    if user is None or user['id'] != id:
        return redirect(url_for("auth.login"))

    viewed_user = db.session.query(User).get(id)

    form = DeleteUserForm(formdata=request.form, obj=viewed_user)

    if form.validate_on_submit():
        pass

    return render_template('user/delete.html', form=form, viewed_user=viewed_user)

# View other user profile. nothing stops a user from passing in their
# own ID, as these are essentially the same
@user.route('/profile/<int:id>')
def view (id):

    user = db.session.query(User).get(id)

    return render_template('user/view.html', viewed_user=user)

