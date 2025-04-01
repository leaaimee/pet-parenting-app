from flask import Blueprint, render_template, redirect, url_for
from backend.forms.user_form import RegistrationForm, LoginForm
from flask_login import current_user



landing_bp = Blueprint("landing", __name__)

@landing_bp.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for("landing.home"))

    return render_template(
        "portal.html",
        login_form=LoginForm(),
        register_form=RegistrationForm(),
        portal_view=True
    )

@landing_bp.route("/home")
def home():
    return render_template("home.html")