from werkzeug.security import generate_password_hash
from backend.database import db
from backend.models.users_models import Users
from backend.utils.upload_helper import get_upload_path

def create_user_profile_data(form):
    """ user creation & password hashing """
    try:
        hashed_password = generate_password_hash(form.password.data)

        new_user = Users(
            name=form.name.data,
            email=form.email.data,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        return new_user

    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}")  # TODO: Replace with proper logging
        return None


def edit_user_profile_data(user, form):
    """ Update user profile with provided fields """
    try:
        user.phone = form.phone.data
        user.location = form.location.data
        user.birth_date = form.birth_date.data
        user.pronouns = form.pronouns.data
        user.languages_spoken = form.languages_spoken.data
        user.experience_with = form.experience_with.data
        user.certifications = form.certifications.data

        print("📦 Data being saved:", user.phone, user.location)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user: {e}")  # TODO: Replace with proper logging
        return None


def get_user_profile(user_id):
    """ Fetch user profile by ID """
    try:
        user = Users.query.get(user_id)
        if not user:
            return None
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")  # TODO: Replace with proper logging
        return None