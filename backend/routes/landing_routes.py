from flask import Blueprint, render_template

landing_bp = Blueprint("landing", __name__)

@landing_bp.route('/')
def home():
    return render_template("index.html")