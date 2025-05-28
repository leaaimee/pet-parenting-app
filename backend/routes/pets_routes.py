import os

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse


from sqlalchemy.orm import Session
from backend.auth.jwt import get_current_user
from backend.database import get_db

from datetime import date


from backend.schemas.pet_schema import PetBasicSchema, PetProfileShowSchema, PetProfileAddSchema, PetProfileEditSchema, \
    PetDataAddSchema, PetDataEditSchema, PetVaccinationAddSchema, PetVaccinationShowSchema, PetVaccinationEditSchema, \
    PetMedicationShowSchema
from backend.schemas.pet_schema import PetMedicalProfileShowSchema,PetMedicalProfileAddSchema, PetMedicalProfileEditSchema
from backend.schemas.pet_schema import PetMedicationAddSchema, PetMedicationEditSchema
from backend.schemas.pet_schema import PetTestResultAddSchema, PetTestResultShowSchema
from backend.schemas.pet_schema import PetTestResultEditSchema
from backend.schemas.pet_schema import PetVetVisitShowSchema, PetVetVisitAddSchema, PetVetVisitEditSchema
from backend.schemas.pet_schema import PetMedicalDocumentShowSchema

from backend.services.pets_service import get_user_pets_service
from backend.services.pets_service import prepare_medical_profile_data_service
from backend.services.pets_service import get_pet_by_id, add_pet_profile_data_service, edit_pet_profile_data_service, prepare_pet_profile_data
from backend.services.pets_service import get_pet_profile_data_service, verify_pet_access
from backend.services.pets_service import edit_pet_data_service
from backend.services.pets_service import add_vaccination_data_service, edit_vaccination_data_service
from backend.services.pets_service import add_medical_profile_data_service, edit_medical_profile_data_service
from backend.services.pets_service import add_pet_data_service, get_medical_profile_data_service, add_medication_data_service, edit_medication_data_service
from backend.services.pets_service import add_test_result_data_service, edit_test_result_data_service
from backend.services.pets_service import add_vet_visit_data_service, edit_vet_visit_data_service
from backend.services.pets_service import add_medical_document_data_service

from backend.utils.upload_helper import get_upload_subpath, VALID_SUBCATEGORIES




router = APIRouter()

@router.get("/pets/family", response_model=list[PetBasicSchema])
def view_pets_family_data(

    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """View all pets owned or cared for by the current user."""
    return get_user_pets_service(current_user["id"], db)




@router.get("/pets/{pet_id}", response_model=PetProfileShowSchema)
def get_pet_profile_data(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Return detailed pet profile including optional pet data"""
    pet = get_pet_profile_data_service(pet_id, current_user["id"], db)

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    return pet



@router.post("/pets/add")
def add_pet_profile_data(
        pet_data: PetProfileAddSchema,
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Create a new pet profile for the logged-in user"""
    pet_dict = prepare_pet_profile_data(pet_data, current_user["id"])
    new_pet = add_pet_profile_data_service(**pet_dict, db=db)

    if not new_pet:
        raise HTTPException(status_code=500, detail="Pet creation failed")

    return {"message": "New pet profile added", "pet_id": new_pet.id}



@router.put("/pets/{pet_id}", response_model=PetProfileShowSchema)
def edit_pet_profile_data(
    pet_id: int,
    data: PetProfileEditSchema,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_pet = edit_pet_profile_data_service(pet_id, current_user["id"], data, db)

    if not updated_pet:
        raise HTTPException(status_code=404, detail="Pet not found or unauthorized")

    return updated_pet



@router.get("/media/pet/{subcategory}/{filename}")
def get_pet_image_data(subcategory: str, filename: str):
    """Serve pet image from a subcategory like portrait/action."""
    if subcategory not in VALID_SUBCATEGORIES["pet"]:
        raise HTTPException(status_code=400, detail="Invalid pet image subcategory")

    file_path = os.path.join(get_upload_subpath("pet", subcategory), filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, media_type="application/octet-stream")



@router.post("/pets/{pet_id}/data", response_model=PetDataAddSchema)
def add_pet_data(
    pet_id: int,
    pet_data: PetDataAddSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_data = add_pet_data_service(pet_id, current_user["id"], pet_data, db)

    if not new_data:
        raise HTTPException(status_code=404, detail="Pet not found or data submission failed")

    return new_data





@router.patch("/pets/{pet_id}/data/edit", response_model=PetDataEditSchema)
def edit_pet_data(
        pet_id:int,
        pet_data: PetDataEditSchema,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    """Edit existing pet data"""
    updated_data = edit_pet_data_service(pet_id, current_user["id"], pet_data, db)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Pet not found or data update failed")

    return updated_data


@router.get("/pets/{pet_id}/medical_data", response_model=PetMedicalProfileShowSchema)
def get_medical_profile_data(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get medical profile for a specific pet"""
    pet = get_pet_by_id(pet_id, db)

    medical_profile = get_medical_profile_data_service(pet_id, current_user["id"], db)

    if not medical_profile:
        raise HTTPException(status_code=404, detail="Medical profile not found")

    return medical_profile



@router.post("/pets/{pet_id}/medical_data", response_model=PetMedicalProfileShowSchema)
def add_medical_profile_data(
    pet_id: int,
    medical_data: PetMedicalProfileAddSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add medical profile for a specific pet"""
    pet = verify_pet_access(pet_id, current_user["id"], db)

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found or unauthorized")

    data = prepare_medical_profile_data_service(medical_data, pet_id, current_user["id"], db)
    new_medical_data = add_medical_profile_data_service(data, db)

    if not new_medical_data:
        raise HTTPException(status_code=500, detail="Medical profile creation failed")

    return new_medical_data


@router.patch("/pets/{pet_id}/medical_data/edit", response_model=PetMedicalProfileEditSchema)
def edit_medical_profile_data(
    pet_id: int,
    medical_data: PetMedicalProfileEditSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Edit existing medical profile for a specific pet"""
    updated_medical_profile = edit_medical_profile_data_service(pet_id, current_user["id"], medical_data, db)

    if not updated_medical_profile:
        raise HTTPException(status_code=404, detail="Medical profile not found or unauthorized")

    return updated_medical_profile



@router.post("/pets/{pet_id}/medical_data/vaccinations", response_model=PetVaccinationShowSchema)
def add_vaccination_data(
        pet_id: int,
        vaccination_data: PetVaccinationAddSchema,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    """Add vaccination record for a specific pet"""
    new_vaccination_data = add_vaccination_data_service(pet_id, vaccination_data, db, current_user["id"])

    if not new_vaccination_data:
        raise HTTPException(status_code=404, detail="Could not add vaccination data")

    return new_vaccination_data


@router.patch("/pets/{pet_id}/medical_data/vaccinations/{vaccination_id}", response_model=PetVaccinationShowSchema)
def edit_vaccination_data(
    pet_id: int,
    vaccination_id: int,
    vaccination_data: PetVaccinationEditSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Edit existing vaccination record for a specific pet"""
    edited_vaccination_data = edit_vaccination_data_service(pet_id, vaccination_id, vaccination_data, db, current_user["id"])

    if not edited_vaccination_data:
        raise HTTPException(status_code=404, detail="Vaccination record not found or unauthorized")

    return edited_vaccination_data



@router.post("/pets/{pet_id}/medical_data/medications", response_model=PetMedicationShowSchema)
def add_medication_data(
    pet_id: int,
    medication_data: PetMedicationAddSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add medication record for a specific pet"""
    new_medication_data = add_medication_data_service(pet_id, medication_data, db, current_user["id"])

    if not new_medication_data:
        raise HTTPException(status_code=404, detail="Could not add medication data")

    return new_medication_data


@router.patch("/pets/{pet_id}/medical_data/medications/{medication_id}", response_model=PetMedicationShowSchema)
def edit_medication_data(
    pet_id: int,
    medication_id: int,
    medication_data: PetMedicationEditSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Edit existing medication record for a specific pet"""
    edited_medication_data = edit_medication_data_service(pet_id, medication_id, medication_data, db, current_user["id"])

    if not edited_medication_data:
        raise HTTPException(status_code=404, detail="Medication record not found or unauthorized")

    return edited_medication_data



@router.post("/pets/{pet_id}/medical_data/test_results", response_model=PetTestResultShowSchema)
def add_test_result_data(
    pet_id: int,
    test_result_data: PetTestResultAddSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add test result record for a specific pet"""
    new_test_result_data = add_test_result_data_service(pet_id, test_result_data, db, current_user["id"])

    if not new_test_result_data:
        raise HTTPException(status_code=404, detail="Could not add test result data")

    return new_test_result_data


@router.patch("/pets/{pet_id}/medical_data/test_results/{test_result_id}", response_model=PetTestResultShowSchema)
def edit_test_result_data(
    pet_id: int,
    test_result_id: int,
    test_result_data: PetTestResultEditSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Edit existing test result record for a specific pet"""
    edited_test_result_data = edit_test_result_data_service(pet_id, test_result_id, test_result_data, db, current_user["id"])

    if not edited_test_result_data:
        raise HTTPException(status_code=404, detail="Test result record not found or unauthorized")

    return edited_test_result_data



@router.post("/pets/{pet_id}/medical_data/vet_visits", response_model=PetVetVisitShowSchema)
def add_vet_visit_data(
    pet_id: int,
    vet_visit_data: PetVetVisitAddSchema = Depends(),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    file: UploadFile | None = None
):
    """Add vet visit record for a specific pet"""
    new_vet_visit_data = add_vet_visit_data_service(
    pet_id,
    vet_visit_data,
    db,
    current_user["id"],
    file
    )

    if not new_vet_visit_data:
        raise HTTPException(status_code=404, detail="Could not add vet visit data")

    return new_vet_visit_data


@router.patch("/pets/{pet_id}/medical_data/vet_visits/{vet_visit_id}", response_model=PetVetVisitShowSchema)
def edit_vet_visit_data(
    pet_id: int,
    vet_visit_id: int,
    vet_visit_data: PetVetVisitEditSchema = Depends(),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    file: UploadFile | None = None
):
    """Edit existing vet visit record for a specific pet"""
    updated_vet_visit = edit_vet_visit_data_service(
        pet_id,
        vet_visit_id,
        vet_visit_data,
        db,
        current_user["id"],
        file
    )

    if not updated_vet_visit:
        raise HTTPException(status_code=404, detail="Vet visit not found or unauthorized")

    return updated_vet_visit



@router.post("/pets/{pet_id}/medical_data/documents", response_model=PetMedicalDocumentShowSchema)
def add_medical_document_data(
    pet_id: int,
    document_name: str = Form(...),
    document_type: str = Form(...),
    upload_date: date = Form(None),
    additional_info: str = Form(None),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    data = prepare_medical_document_data(
        pet_id, document_name, document_type, upload_date, additional_info, file
    )
    result = add_medical_document_data_service(data, db, current_user["id"])
    if not result:
        raise HTTPException(status_code=404, detail="Something went wrong")
    return result


