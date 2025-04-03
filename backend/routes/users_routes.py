from flask import Blueprint, render_template, redirect, url_for, request, redirect
from flask_login import login_required, current_user, login_url, login_user, logout_user
from backend.forms.user_form import RegistrationForm, LoginForm
from backend.models.users_models import Users, db
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint("users", __name__)


@users_bp.route('/user-profile')
# @login_required
def user_profile():
    return render_template("show_user_profile.html", user=current_user)


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = Users(
            name=form.name.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('landing.profile'))

    return render_template("landing.html", register_form=form, login_form=LoginForm())


@users_bp.route("/login", methods=["POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('landing.home'))  # Or whatever page comes next
    return redirect(url_for('landing.portal'))


@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("landing.home"))


@users_bp.route('/edit-profile', methods=['GET', 'POST'])
# @login_required
def edit_user_profile():
    return "Edit Profile Page Coming Soon!"