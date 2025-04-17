from flask import Blueprint, render_template, redirect, url_for, request, redirect
from flask import jsonify, url_for, send_from_directory
from flask_login import login_required, current_user, login_url, login_user, logout_user
from backend.forms.user_form import RegistrationForm, LoginForm, EditUserProfileForm
from backend.models.users_models import Users, db
from werkzeug.security import generate_password_hash, check_password_hash
from backend.services.users_service import get_user_profile, edit_user_profile_data, create_user_profile_data
from backend.utils.upload_helper import get_upload_path
users_bp = Blueprint("users", __name__)
from flask_jwt_extended import create_access_token
from backend.models.users_models import Users



@users_bp.route('/user-profile')
@login_required
def user_profile():
    return render_template("show_user_profile.html", user=current_user)


@users_bp.route('/add_user_profile', methods=['GET', 'POST'])
def add_user_profile():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = create_user_profile_data(form)

        if new_user:
            login_user(new_user)
            return redirect(url_for('users.show_user_profile', user_id=new_user.id))

    return render_template("landing.html", register_form=form, login_form=LoginForm())


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('landing.home'))

    return redirect(url_for('landing.home'))


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing.home"))


@users_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_user_profile():
    form = EditUserProfileForm(obj=current_user)

    if form.validate_on_submit():
        edit_user_profile_data(current_user, form)

        return redirect(url_for('users.show_user_profile', user=current_user))

    return render_template("edit_user_profile.html", form=form, user=current_user)


@users_bp.route('/media/user/<filename>')
def user_image(filename):
    return send_from_directory(get_upload_path("user"), filename)


@users_bp.route('/profile/', methods=['GET'])
@login_required
def show_user_profile():
    user = get_user_profile(current_user.id)
    if not user:
        return "User not found", 404
    return render_template("show_user_profile.html", user=user)


@users_bp.route("/token", methods=["POST"])
def get_token():
    username = request.json.get("username")
    if not username:
        return jsonify({"msg": "Missing username"}), 400

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)




from flask_jwt_extended import jwt_required, get_jwt_identity

@users_bp.route("/whoami", methods=["GET"])
@jwt_required()
def whoami():
    """
    Get current authenticated user
    ---
    tags:
      - Users
    responses:
      200:
        description: Returns the current user's name
        examples:
          application/json: { "message": "Hello, Ellen Ripley" }
    """
    current_user = get_jwt_identity()
    return jsonify(message=f"Hello: {current_user}"), 200


@users_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected_route():
    current_identity = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_identity}. You're in a secure zone."}), 200

