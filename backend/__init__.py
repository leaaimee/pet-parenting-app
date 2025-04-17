from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from .database import db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from backend.models.invitations_models import *
from backend.routes.landing_routes import landing_bp
from backend.routes.pets_routes import pets_bp
from backend.routes.users_routes import users_bp
from backend.routes.invitations_routes import invitations_bp
from backend.models.users_models import Users




# 🛠️ Flask app factory
def create_app():
    app = Flask(__name__, template_folder="../templates")

    load_dotenv()

    # 🔐 Config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SESSION_COOKIE_SECURE"] = False

    # JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    # JWT setup
    jwt = JWTManager(app)

    # Swagger
    swagger = Swagger(app)

    # 📦 File upload config
    base_upload = os.path.join(os.getcwd(), 'backend', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    app.config['PET_IMAGE_UPLOAD_FOLDER'] = os.path.join(base_upload, 'pet_images')
    app.config['USER_IMAGE_UPLOAD_FOLDER'] = os.path.join(base_upload, 'user_images')
    app.config['MEDICAL_UPLOAD_FOLDER'] = os.path.join(base_upload, 'medical_docs')


    # 🔌 Init extensions
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "landing.landing"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # 🌐 Register routes
    app.register_blueprint(landing_bp)
    app.register_blueprint(pets_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(invitations_bp)

    return app