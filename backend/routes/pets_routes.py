from flask import Blueprint, render_template, request, redirect, url_for, abort, send_from_directory
from flask_login import current_user, login_required
from backend.forms.pet_form import PetForm, PetDataForm, MedicalProfileForm
from backend.models.pets_models import Pets, PetData, MedicalProfile, db
from backend.services.pets_service import add_pet_data_data, prepare_medical_profile_data, edit_medical_profile
from backend.services.pets_service import add_medication_data, add_vaccination_data, add_test_result_data, add_vet_visit_data, add_medical_document_data
from backend.services.pets_service import get_pet_by_id, add_pet_profile_data, edit_pet_profile_data, prepare_pet_profile, prepare_pet_data

from backend.utils.upload_helper import get_upload_path
from backend.forms.pet_form import VaccinationRecordForm, MedicationForm, TestResultsForm, VetVisitForm, MedicalDocumentForm
from datetime import datetime

pets_bp = Blueprint("pets", __name__)


@pets_bp.route("/pets/<int:pet_id>")
@login_required
def pet_profile(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        abort(404, description="Pet not found.")

    pet_data = PetData.query.filter_by(pet_id=pet_id).first()

    return render_template("show_pet_profile.html", pet=pet, pet_data=pet_data)


@pets_bp.route("/pets/add", methods = ["GET", "POST"])
@login_required
def add_pet_profile():
    form = PetForm()

    if form.validate_on_submit():
        pet_data = prepare_pet_profile(form, current_user.id)
        new_pet = add_pet_profile_data(**pet_data)

        if not new_pet:
            return "Pet creation failed", 500

        return redirect(url_for('pets.pet_profile', pet_id=new_pet.id))

    return render_template('new_pet_profile.html', form=form)


@pets_bp.route("/pets/<int:pet_id>/edit", methods=["GET", "POST"])
@login_required
def edit_pet_profile(pet_id):

    pet = Pets.query.get_or_404(pet_id)
    form = PetForm(obj=pet)

    if form.validate_on_submit():
        updated_pet = edit_pet_profile_data(pet_id, current_user.id)

        if not updated_pet:
            return "Unauthorized or failed update", 403

        return redirect(url_for("pets.pet_profile", pet_id=pet.id))

    return render_template("edit_pet_profile.html", form=form, pet=pet)


@pets_bp.route('/media/pet/<filename>')
def pet_image(filename):
    return send_from_directory(get_upload_path("pet"), filename)


@pets_bp.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory(get_upload_path("medical"), filename)


@pets_bp.route("/pets/<int:pet_id>/data/add", methods=["GET", "POST"])
@login_required
def add_pet_data(pet_id):
    form = PetDataForm()
    if request.method == "POST" and form.validate_on_submit():
        data = prepare_pet_data(form, pet_id, current_user.id)
        add_pet_data_data(**data)
        print(f"✅ Pet data submitted for pet_id: {pet_id}")  # <<-- Here!
        return redirect(url_for('pets.pet_profile', pet_id=pet_id))
    return render_template("add_pet_data.html", form=form, pet_it=pet_id)


@pets_bp.route("/pets/<int:pet_id>/data/edit", methods=["GET", "POST"])
@login_required
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
@login_required
def show_pets():
    pets = Pets.query.filter_by(parent_id=current_user.id).all()

    return render_template("pet_family.html", pets=pets)


@pets_bp.route("/pets/<int:pet_id>/medical_data", methods=["GET", "POST"])
@login_required
def medical_data(pet_id):
    pet = Pets.query.get_or_404(pet_id)
    medical_profile = MedicalProfile.query.filter_by(pet_id=pet_id).first()

    if medical_profile:
        test_results = sorted(
            medical_profile.test_results,
            key=lambda r: r.date or datetime.min,
            reverse=True
        )
    else:
        test_results = []



    return render_template("medical_data.html",
                           pet=pet,
                           medical_profile=medical_profile,
                           test_results=test_results)


@pets_bp.route("/pets/<int:pet_id>/medical_data/edit", methods=["GET", "POST"])
@login_required
def edit_medical_data(pet_id):
    pet = Pets.query.get_or_404(pet_id)
    existing_profile = MedicalProfile.query.filter_by(pet_id=pet_id).first()

    form = MedicalProfileForm(obj=existing_profile)

    if form.validate_on_submit():
        data = prepare_medical_profile_data(form, pet_id)
        updated_profile = edit_medical_profile(**data)
        if updated_profile:
            return redirect(url_for("pets.medical_data", pet_id=pet.id))


    return render_template(
        "edit_medical_data.html",
        form=form,
        vaccine_form=VaccinationRecordForm(),
        medication_form=MedicationForm(),
        test_form=TestResultsForm(),
        vet_visit_form=VetVisitForm(),
        document_form=MedicalDocumentForm(),
        pet=pet,
        pet_id=pet_id
    )


# @pets_bp.route("/pets/<int:pet_id>/medical_data/edit_vaccination", methods=["POST"])
# @login_required
# def edit_vaccination(pet_id):
#     form= VaccinationRecordForm()
#
#     if form.validate_on_submit():
#         if not edit_vaccination_data(pet_id, form):
#             return "Medical profile not found", 404
#
#     return redirect(url_for('pets.edit_medical_data', pet_id=pet_id))

@pets_bp.route("/pets/<int:pet_id>/medical_data/add_vaccination", methods=["POST"])
@login_required
def add_vaccination(pet_id):
    form = VaccinationRecordForm()

    if form.validate_on_submit():
        print("✅ Vaccine form validated successfully.")
        result = add_vaccination_data(pet_id, form)
        if not result:
            print("❌ Vaccination data was not saved — profile missing?")
            return "Medical profile not found", 404
    else:
        print("❌ Vaccine form validation failed.")
        print("🔍 Form errors:", form.errors)

    return redirect(url_for('pets.edit_medical_data', pet_id=pet_id))


@pets_bp.route("/pets/<int:pet_id>/medical_data/add_medication", methods=["POST"])
@login_required
def add_medication(pet_id):
    form= MedicationForm()

    if form.validate_on_submit():
        if not add_medication_data(pet_id, form):
            return "Medical profile not found", 404

    return redirect(url_for('pets.edit_medical_data', pet_id=pet_id))


@pets_bp.route("/pets/<int:pet_id>/medical_data/add_test_results", methods=["POST"])
@login_required
def add_test_result(pet_id):
    form= TestResultsForm()

    if form.validate_on_submit():
        if not add_test_result_data(pet_id, form):
            return "Medical profile not found", 404

    return redirect(url_for('pets.edit_medical_data', pet_id=pet_id))


@pets_bp.route("/pets/<int:pet_id>/medical_data/add_vet_visit", methods=["POST"])
@login_required
def add_vet_visit(pet_id):
    form= VetVisitForm()

    if form.validate_on_submit():
        if not add_vet_visit_data(pet_id, form):
            return "Medical profile not found", 404

    return redirect(url_for('pets.edit_medical_data', pet_id=pet_id))


@pets_bp.route("/pets/<int:pet_id>/medical_data/add_medical_document", methods=["POST"])
@login_required
def add_medical_document(pet_id):
    form= MedicalDocumentForm()

    if form.validate_on_submit():
        if not add_medical_document_data(pet_id, form):
            return "Medical profile not found", 404

    return redirect(url_for('pets.edit_medical_data', pet_id=pet_id))