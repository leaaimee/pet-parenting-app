from backend import Permissions
from backend.models.pets_models import Pets
from backend.database import db
from datetime import date, datetime
from flask import request
from sqlalchemy.exc import SQLAlchemyError

from backend.utils.permissions import user_has_access


def get_pet_by_id(pet_id):
    """ Fetch a pet profile by ID """
    pet = Pets.query.get(pet_id)
    if not pet:
        return None
    return pet

def pet_birthday(birth_year, birth_month, birth_day):
    """ setting exact or approximate birthday date """
    try:
        current_year = datetime.now().year

        birth_year = int(birth_year) if birth_year and birth_year.isdigit() and 1900 <= int(birth_year) <= current_year else None
        birth_month = int(birth_month) if birth_month and birth_month.isdigit() and 1 <= int(birth_month) <= 12 else None
        birth_day = int(birth_day) if birth_day and birth_day.isdigit() else None

        if birth_year is not None and birth_month is not None and birth_day is not None:
            try:
                return date(birth_year, birth_month, birth_day), None, None
            except ValueError:
                return None, None, None

        if birth_year is not None and birth_month is not None:
            return None, birth_year, birth_month

        if birth_year is not None:
            return None, birth_year, None


    except Exception as e:
        print(f"Unexpected error in pet_birthday: {e}")
        return None, None, None

    return None, None, None


def prepare_pet_data(form, parent_id):
    """ Extracts and processes pet form data for storage """
    name = form.get["name"].strip()
    species = form["species"].strip()
    subspecies = form.get("subspecies", None)
    description = form.get("profile_description", None)
    profile_picture = form.get("profile_picture", None)

    birth_day = int(form.get("birth_day")) if form.get("birth_day", "").isdigit() else None
    birth_month = int(form.get("birth_month")) if form.get("birth_month", "").isdigit() else None
    birth_year = int(form.get("birth_year")) if form.get("birth_year", "").isdigit() else None

    birthday, birth_year, birth_month = pet_birthday(birth_year, birth_month, birth_day)

    return {
        "name": name,
        "species": species,
        "subspecies": subspecies,
        "birthday": birthday,
        "birth_year": birth_year,
        "birth_month": birth_month,
        "description": description,
        "profile_picture": profile_picture,
        "parent_id": parent_id
    }


def create_pet_profile(name, species, subspecies, birth_year, birth_month, birthday, description, profile_picture, parent_id):
    """ Create new pet profile """
    try:
        new_pet = Pets(
            name=name,
            species=species,
            subspecies=subspecies,
            birthday=birthday,
            birth_year=birth_year,
            birth_month=birth_month,
            description=description,
            profile_picture=profile_picture,
            parent_id=parent_id
        )

        db.session.add(new_pet)
        db.session.commit()

        return new_pet


    except SQLAlchemyError:
        db.session.rollback()
        return None  # TODO: Improve error handling later

    except Exception:
        db.session.rollback()
        return None


def update_pet_profile(pet_id, user_id):
    try:
        pet = Pets.query.get(pet_id)
        if not pet:
            return None

        if pet.parent_id != user_id and not user_has_access(user_id, pet_id, Permissions.EDIT_PET_INFO):
            return None

        pet.name = request.form.get("name", pet.name)
        pet.species = request.form.get("species", pet.species)
        pet.subspecies = request.form.get("subspecies", pet.subspecies)
        pet.description = request.form.get("description", pet.description)
        pet.profile_picture = request.form.get("profile_picture", pet.profile_picture)

        birth_day = request.form.get("birth_day", "").strip() or None
        birth_month = request.form.get("birth_month", "").strip() or None
        birth_year = request.form.get("birth_year", "").strip() or None

        pet.birthday, pet.birth_year, pet.birth_month = pet_birthday(birth_year, birth_month, birth_day)

        db.session.commit()
        return pet

    except SQLAlchemyError:
        db.session.rollback()
        return None


