from werkzeug.security import generate_password_hash
from backend.database import db
from backend.models.users_models import Users

def create_user_profile(name, email, password):
    """ user creation & password hashing """
    try:
        hashed_password = generate_password_hash(password)

        new_user = Users(
            name=name,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.commit()
        return new_user

    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}")  # TODO: Replace with proper logging
        return None