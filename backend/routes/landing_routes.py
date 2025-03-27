from flask import Blueprint, render_template
from backend.forms.user_form import RegistrationForm, LoginForm


landing_bp = Blueprint("landing", __name__)

@landing_bp.route('/')
def landing():
    return render_template(
        "portal.html",
        login_form=LoginForm(),
        register_form=RegistrationForm(),
        portal_view = True
    )