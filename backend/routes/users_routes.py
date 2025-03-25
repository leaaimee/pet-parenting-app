from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from backend.forms.user_form import RegistrationForm
from backend.models.users_models import Users, db
from werkzeug.security import generate_password_hash

users_bp = Blueprint("users", __name__)

@users_bp.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = Users(
            name=form.name.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        db.session.add()
        db.session.commit()
        return redirect(url_for('users.profile'))

    return render_template("register.html", form=form)



    # if request.method == "POST":
    #     name = request.form["name"]
    #     email = request.form["email"]
    #     password = request.form["password"]
    #
    #     new_user = create_user_profile(name, email,password)
    #
    #     if new_user:
    #         return redirect(url_for('users.profile'))

    # return render_template('register.html')