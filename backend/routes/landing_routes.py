from flask import Blueprint, render_template, redirect, url_for
from backend.forms.user_form import RegistrationForm, LoginForm
from flask_login import current_user, login_required



landing_bp = Blueprint("landing", __name__)

@landing_bp.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for("landing.home"))

    return render_template(
        "landing.html",
        login_form=LoginForm(),
        register_form=RegistrationForm(),
        portal_view=True
    )

@landing_bp.route("/home")
@login_required
def home():
    print("Current user:", current_user)
    print("Authenticated?", current_user.is_authenticated)
    return render_template("home.html", user=current_user)



