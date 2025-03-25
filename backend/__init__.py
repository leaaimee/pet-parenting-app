from flask import Flask
from flask_migrate import Migrate
from .database import db
from dotenv import load_dotenv
import os

from backend.models.invitations_models import *
from backend.routes.landing_routes import landing_bp
from backend.routes.pets_routes import pets_bp
from backend.routes.users_routes import users_bp


def create_app():
    app = Flask(__name__, template_folder="../templates")

    load_dotenv()

    # Configuration for the app
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


    # Initialize the database and migrations
    db.init_app(app)
    Migrate(app, db)

    # Register the blueprint for routes
    app.register_blueprint(landing_bp)
    app.register_blueprint(pets_bp)  # Register pet routes
    app.register_blueprint(users_bp)  # Register user routes

    return app