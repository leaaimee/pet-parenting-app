from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user

from backend.services.pets_service import get_pet_by_id, create_pet_profile, update_pet_profile, prepare_pet_data
from backend.utils.constants import RoleType


pets_bp = Blueprint("pets", __name__)


@pets_bp.route("/profile/<int:pets_id>")
def pet_profile(pets_id):
    pet = get_pet_by_id(pets_id)
    if not pet:
        abort(404, description="Pet not found.")
    return render_template("pet_profile.html", pet=pet)


@pets_bp.route("/add", methods = ["GET", "POST"])
def add_pet_profile():
    if request.method == "POST":
        pet_data = prepare_pet_data(request.form, current_user.id)
        new_pet = create_pet_profile(**pet_data)

        return redirect(url_for('pets.pet_profile', pets_id=new_pet.id))

    return render_template('add_pet.html')


@pets_bp.route("/profile/<int:pets_id>/update", methods=["PATCH"])
def update_pet_data(pets_id):

    updated_pet = update_pet_profile(pets_id, current_user.id)

    if not updated_pet:
        abort(404, description="Pet Profile not found")

    return redirect(url_for('pets.pet_profile', pets_id=updated_pet.id))



@pets_bp.route("/pet-family")
def show_pets():
    user_pets = [role.pet for role in current_user.roles if role.role == RoleType.OWNER]
    friend_pets = [role.pet for role in current_user.roles if role.role != RoleType.OWNER]

    # NOTE: Consider refining the empty pet case handling later.
    # Possible improvements:
    # 1️⃣ Prevent repetitive flash messages
    # 2️⃣ Smarter UI prompt for new users vs. users who deleted pets
    # 3️⃣ A more elegant logic for guiding first-time users

    return render_template("pet_family.html", user_pets=user_pets, friend_pets=friend_pets)