from backend import Permissions, db
from backend.models.pets_models import Pets, PetData, MedicalProfile
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

        if isinstance(birth_year, int) and 1900 <= birth_year <= current_year:
            if isinstance(birth_month, int) and 1 <= birth_month <= 12:
                if isinstance(birth_day, int):
                    try:
                        return date(birth_year, birth_month, birth_day), None, None
                    except ValueError:
                        return None, None, None
                return None, birth_year, birth_month
            return None, birth_year, None
        return None, None, None

    except Exception as e:
        print("Unexpected error in pet_birthday:", e)
        return None, None, None


def prepare_pet_profile(form, parent_id):
    """ Extracts and processes pet form data for storage """
    name = form.name.data.strip()
    species = form.species.data.strip()
    subspecies = form.subspecies.data or None
    gender = form.gender.data or None
    profile_description = form.profile_description.data or None
    profile_picture = form.profile_picture.data or None

    birth_day = form.birthday.data.day if form.birthday.data else None
    birth_month = int(form.birth_month.data) if form.birth_month.data else None
    birth_year = int(form.birth_year.data) if form.birth_year.data else None

    birthday, birth_year, birth_month = pet_birthday(birth_year, birth_month, birth_day)

    return {
        "name": name,
        "species": species,
        "subspecies": subspecies,
        "gender": gender,
        "birthday": birthday,
        "birth_year": birth_year,
        "birth_month": birth_month,
        "description": profile_description,
        "profile_picture": profile_picture,
        "parent_id": parent_id
    }


def create_pet_profile(name, species, subspecies, gender, birth_year, birth_month, birthday, description, profile_picture, parent_id):
    """ Create new pet profile """
    try:
        new_pet = Pets(
            name=name,
            species=species,
            subspecies=subspecies,
            gender=gender,
            birthday=birthday,
            birth_year=birth_year,
            birth_month=birth_month,
            profile_description=description,
            profile_picture=profile_picture,
            parent_id=parent_id
        )

        db.session.add(new_pet)
        db.session.commit()

        return new_pet


    except SQLAlchemyError as e:
        db.session.rollback()
        print("❌ SQLAlchemyError during pet creation:", e)
        return None

    except Exception as e:
        db.session.rollback()
        print("❌ General Exception during pet creation:", e)
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



def prepare_pet_data(form, pet_id, user_id):
    """ Extracts and processes pet additional data for storage """
    return {
        "favorite_things": form.favorite_things.data or None,
        "dislikes": form.dislikes.data or None,
        "preferred_treats": form.preferred_treats.data or None,
        "social_style": form.social_style.data or None,
        "allergies": form.allergies.data or None,
        "medical_alerts": form.medical_alerts.data or None,
        "diet": form.diet.data or None,
        "communication": form.communication.data or None,
        "behavior_notes": form.behavior_notes.data or None,
        "additional_info": form.additional_info.data or None,
        "pet_id": pet_id,
        "user_id": user_id
    }



def create_pet_data(favorite_things, dislikes, preferred_treats, social_style, allergies, medical_alerts, diet, communication, behavior_notes, additional_info, pet_id, user_id):
    try:

        pet = Pets.query.get(pet_id)
        if not pet or pet.parent_id != user_id:
            return None

        pet_data = PetData (
            favorite_things=favorite_things,
            dislikes=dislikes,
            social_style=social_style,
            communication=communication,
            preferred_treats=preferred_treats,
            diet=diet,
            allergies=allergies,
            medical_alerts=medical_alerts,
            behavior_notes=behavior_notes,
            additional_info=additional_info,
            pet_id = pet_id,
            user_id = user_id
        )

        db.session.add(pet_data)
        db.session.commit()

        return pet_data


    except SQLAlchemyError:
        db.session.rollback()
        return None  # TODO: Improve error handling later

    except Exception:
        db.session.rollback()
        return None


def edit_pet_data(pet_id, user_id):
    try:

        pet_data = PetData.query.filter_by(pet_id=pet_id).first()
        pet = Pets.query.get(pet_id)

        if not pet_data or not pet:
            return None

        if pet.parent_id != user_id and not user_has_access(user_id, pet_id, Permissions.EDIT_PET_INFO):
            return None


        pet_data.favorite_things = request.form.get("favorite_things", pet_data.favorite_things)
        pet_data.dislikes = request.form.get("dislikes", pet_data.dislikes)
        pet_data.social_style = request.form.get("social_style", pet_data.social_style)
        pet_data.communication = request.form.get("communication", pet_data.communication)
        pet_data.preferred_treats = request.form.get("preferred_treats", pet_data.preferred_treats)
        pet_data.diet = request.form.get("diet", pet_data.diet)
        pet_data.allergies = request.form.get("allergies", pet_data.allergies)
        pet_data.medical_alerts = request.form.get("medical_alerts", pet_data.medical_alerts)
        pet_data.behavior_notes = request.form.get("behavior_notes", pet_data.behavior_notes)
        pet_data.additional_info = request.form.get("additional_info", pet_data.additional_info)

        db.session.commit()
        return pet_data

    except SQLAlchemyError:
        db.session.rollback()
        return None

    except Exception:
        db.session.rollback()
        return None




def prepare_medical_profile_data(form, pet_id):
    return {
        "pet_id": pet_id,
        "blood_type": form.blood_type.data or None,
        "weight": form.weight.data or None,
        "weight_updated": form.weight_updated.data or None,
        "chronic_conditions": form.chronic_conditions.data or None,
        "notes": form.notes.data or None,
    }


def edit_medical_profile(**data):
    existing_profile = MedicalProfile.query.filter_by(pet_id=data["pet_id"]).first()

    if existing_profile:
        for key, value in data.items():
            setattr(existing_profile, key, value)
    else:
        existing_profile = MedicalProfile(**data)
        db.session.add(existing_profile)

    db.session.commit()
    return existing_profile