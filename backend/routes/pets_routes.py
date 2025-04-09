from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user
from backend.forms.pet_form import PetForm, PetDataForm
from backend.models.pets_models import Pets, PetData, db
from backend.services.pets_service import create_pet_data

from backend.services.pets_service import get_pet_by_id, create_pet_profile, update_pet_profile, prepare_pet_profile
from backend.utils.constants import RoleType


pets_bp = Blueprint("pets", __name__)


@pets_bp.route("/pets/<int:pets_id>")
def pet_profile(pets_id):
    pet = get_pet_by_id(pets_id)
    if not pet:
        abort(404, description="Pet not found.")
    return render_template("show_pet_profile.html", pet=pet)


@pets_bp.route("/pets/add", methods = ["GET", "POST"])
def add_pet_profile():
    form = PetForm()
    if request.method == "POST":
        pet_data = prepare_pet_profile(request.form, current_user.id)
        new_pet = create_pet_profile(**pet_data)

        return redirect(url_for('pets.pet_profile', pet_id=new_pet.id))

    return render_template('new_pet_profile.html', form=form)


@pets_bp.route("/pets/<int:pets_id>/edit", methods=["GET", "POST"])
def edit_pet_profile(pet_id):

    pet = Pets.query.get_or_404(pet_id)

    form = PetForm(obj=pet)

    if form.validate_on_submit():
        form.populate_obj(pet)  # Updates the pet object with form data
        db.session.commit()
        return redirect(url_for("pets.pet_profile", pet_id=pet.id))

    return render_template("edit_pet_profile.html", form=form, pet=pet)


@pets_bp.route("/pets/<int:pet_id>/data/add", methods=["GET", "POST"])
def add_pet_data(pet_id):
    form = PetDataForm()
    if request.method == "POST" and form.validate_on_submit():
        data = prepare_pet_profile(form, pet_id)
        create_pet_data(**data)
        return redirect(url_for('pets.pet_profile', pet_id=pet_id))
    return render_template("add_pet_data.html", form=form, pet_it=pet_id)


@pets_bp.route("/pets/<int:pet_id>/data/add", methods=["GET", "POST"])
def edit_pet_data(pet_id):

    pet = Pets.query.get_or_404(pet_id)
    pet_data = PetData.query.filter_by(pet_id=pet_id).first()

    if not pet_data:
        pet_data = PetData(pet_id=pet_id)
        db.session.add(pet_data)

    form = PetDataForm(obj=pet_data)

    if form.validate_on_submit():
        form.populate_obj(pet_data)
        db.session.commit()
        return redirect(url_for("pets.pet_profile", pet_id=pet.id))

    return render_template("edit_pet_data.html", form=form, pet_id=pet_id)


# 🔜 TODO: Display vaccination history in pet profile page
# vaccination_history = VaccinationRecord.query.filter_by(pet_id=pet.id).order_by(VaccinationRecord.date_administered.desc()).all()

@pets_bp.route("/pet-family")
def show_pets():
    return render_template("pet_family.html")
    # user_pets = [role.pet for role in current_user.roles if role.role == RoleType.OWNER]
    # friend_pets = [role.pet for role in current_user.roles if role.role != RoleType.OWNER]

    # NOTE: Consider refining the empty pet case handling later.
    # Possible improvements:
    # 1️⃣ Prevent repetitive flash messages
    # 2️⃣ Smarter UI prompt for new users vs. users who deleted pets
    # 3️⃣ A more elegant logic for guiding first-time users

    # return render_template("pet_family.html", user_pets=user_pets, friend_pets=friend_pets)


@pets_bp.route("/pets/<int:pet_id>/medical_data", methods=["GET", "POST"])
def medical_data(pet_id):
    pass