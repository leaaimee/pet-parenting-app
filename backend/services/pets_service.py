from backend import Permissions, db
from backend.models.pets_models import Pets, PetData, MedicalProfile, Medication, VaccinationRecord, TestResult, VetVisit, MedicalDocument
from backend.database import db
from datetime import date, datetime
from flask import request, current_app
from sqlalchemy.exc import SQLAlchemyError
from backend.utils.file_utils import save_file
from backend.utils.upload_helper import get_upload_path
import os

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

    file = form.profile_picture.data
    profile_picture = save_file(file, get_upload_path("pet")) if file else ""

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


def add_pet_profile_data(name, species, subspecies, gender, birth_year, birth_month, birthday, description, profile_picture, parent_id):
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


def edit_pet_profile_data(pet_id, user_id):
    try:
        pet = Pets.query.get(pet_id)
        if not pet:
            return None

        if pet.parent_id != user_id and not user_has_access(user_id, pet_id, Permissions.EDIT_PET_INFO):
            return None

        pet.name = request.form.get("name", pet.name)
        pet.species = request.form.get("species", pet.species)
        pet.subspecies = request.form.get("subspecies", pet.subspecies)
        pet.profile_description = request.form.get("description", pet.profile_description)

        file = request.files.get("profile_picture")
        if file:
            filename = save_file(file, get_upload_path("pet"))
            if filename:
                pet.profile_picture = filename

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



def add_pet_data_data(favorite_things, dislikes, preferred_treats, social_style, allergies, medical_alerts, diet, communication, behavior_notes, additional_info, pet_id, user_id):
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


def edit_pet_data_data(pet_id, user_id):
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


def handle_pet_image_upload(file):
    if file:
        return save_file(file, current_app.config['UPLOAD_FOLDER'])
    return ""


# profile helper function
def ensure_medical_profile(pet_id):
    profile = MedicalProfile.query.filter_by(pet_id=pet_id).first()
    if not profile:
        print(f"❌ No medical profile found for pet {pet_id}")
    return profile


def add_vaccination_data(pet_id, form):
    profile = ensure_medical_profile(pet_id)
    if not profile:
        return None

    vaccination_record = VaccinationRecord(
        pet_id=pet_id,
        medical_profile_id=profile.id,
        vaccine_name=form.vaccine_name.data,
        dose_number=form.dose_number.data,
        batch_number=form.batch_number.data,
        previous_vaccination_date=form.previous_vaccination_date.data,
        next_vaccination_date=form.next_vaccination_date.data,
        additional_info=form.additional_info.data,
    )

    db.session.add(vaccination_record)
    db.session.commit()
    return vaccination_record


def add_medication_data(pet_id, form):
    profile = ensure_medical_profile(pet_id)
    if not profile:
        return None

    new_med = Medication(
        pet_id=pet_id,
        medical_profile_id=profile.id,
        name=form.name.data,
        dosage=form.dosage.data,
        duration=form.duration.data,
        additional_info=form.additional_info.data,
    )

    db.session.add(new_med)
    db.session.commit()
    return new_med


def add_test_result_data(pet_id, form):
    profile = ensure_medical_profile(pet_id)
    if not profile:
        return None

    new_test_result = TestResult(
        pet_id=pet_id,
        medical_profile_id=profile.id,
        test_type=form.test_type.data,
        result=form.result.data,
        date=form.date.data,
        additional_info=form.additional_info.data,
    )

    db.session.add(new_test_result)
    db.session.commit()
    return new_test_result


def add_vet_visit_data(pet_id, form):
    profile = ensure_medical_profile(pet_id)
    if not profile:
        return None

    file = request.files.get("document")
    filename = save_file(file, get_upload_path("medical")) if file else ""

    new_vet_visit = VetVisit(
        pet_id=pet_id,
        medical_profile_id=profile.id,
        reason=form.reason.data,
        vet_name=form.vet_name.data,
        clinic_info=form.clinic_info.data,
        date=form.date.data,
        documents=filename,
    )

    db.session.add(new_vet_visit)
    db.session.commit()
    return new_vet_visit


def add_medical_document_data(pet_id, form):
    profile = ensure_medical_profile(pet_id)
    if not profile:
        return None

    file = request.files.get("file")
    filename = save_file(file, get_upload_path("medical")) if file else ""

    new_medical_document = MedicalDocument(
        pet_id=pet_id,
        medical_profile_id=profile.id,
        file_path=filename,
        description=form.description.data,
        uploaded_at=form.uploaded_at.data,
    )

    db.session.add(new_medical_document)
    db.session.commit()
    return new_medical_document