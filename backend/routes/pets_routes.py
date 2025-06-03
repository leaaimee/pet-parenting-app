import os
import mimetypes

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form

from sqlalchemy.ext.asyncio import AsyncSession


from fastapi.responses import FileResponse

from backend.database import get_async_session

from sqlalchemy.orm import Session

from sqlalchemy.future import select


from backend.auth.jwt import get_current_user
# from backend.database import get_db

from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession


from backend.schemas.media_schema import MediaBaseShowSchema



from backend.schemas.pet_schema import PetBasicSchema, PetProfileShowSchema, PetProfileAddSchema, PetProfileEditSchema, \
    PetDataAddSchema, PetDataEditSchema, PetVaccinationAddSchema, PetVaccinationShowSchema, PetVaccinationEditSchema, \
    PetMedicationShowSchema
from backend.schemas.pet_schema import PetMedicalProfileShowSchema,PetMedicalProfileAddSchema, PetMedicalProfileEditSchema
from backend.schemas.pet_schema import PetMedicationAddSchema, PetMedicationEditSchema
from backend.schemas.pet_schema import PetTestResultAddSchema, PetTestResultShowSchema
from backend.schemas.pet_schema import PetTestResultEditSchema
from backend.schemas.pet_schema import PetVetVisitShowSchema, PetVetVisitAddSchema, PetVetVisitEditSchema
from backend.schemas.pet_schema import PetMedicalDocumentShowSchema, PetMedicalDocumentAddSchema, PetMedicalDocumentEditSchema

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
from backend.services.pets_service import add_medical_document_service, edit_medical_document_service
from backend.services.pets_service import add_pet_profile_image_service

from backend.utils.upload_helper import get_upload_subpath, VALID_SUBCATEGORIES




router = APIRouter()

@router.get("/pets/family", response_model=list[PetBasicSchema])
async def view_pets_family_data(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """View all pets owned or cared for by the current user."""
    return await get_user_pets_service(current_user["id"], session)




@router.get("/pets/{pet_id}", response_model=PetProfileShowSchema)
async def get_pet_profile_data(
    pet_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Return detailed pet profile including optional pet data"""
    pet = await get_pet_profile_data_service(pet_id, current_user["id"], session)

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    return pet



@router.post("/pets", response_model=PetProfileShowSchema)
async def add_pet_profile_data(
    pet_data: PetProfileAddSchema,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new pet profile for the logged-in user"""
    pet_dict = prepare_pet_profile_data(pet_data, current_user["id"])
    new_pet = await add_pet_profile_data_service(**pet_dict, session=session)

    if not new_pet:
        raise HTTPException(status_code=500, detail="Pet creation failed")

    return {"message": "New pet profile added", "pet_id": new_pet.id}




@router.patch("/pets/{pet_id}", response_model=PetProfileShowSchema)
async def edit_pet_profile_data(
    pet_id: int,
    data: PetProfileEditSchema,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    updated_pet = await edit_pet_profile_data_service(pet_id, current_user["id"], data, session)

    if not updated_pet:
        raise HTTPException(status_code=404, detail="Pet not found or unauthorized")

    return updated_pet



@router.post("/pets/{pet_id}/image", response_model=MediaBaseShowSchema)
async def add_pet_profile_image_data(
    pet_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    uploaded_file = await add_pet_profile_image_service(session, file, pet_id)
    return uploaded_file



@router.get("/media/pet/{subcategory}/{filename}")
def get_pet_profile_image_data(subcategory: str, filename: str):
    """Serve pet image from a subcategory like portrait/action."""
    if subcategory not in VALID_SUBCATEGORIES["pet"]:
        raise HTTPException(status_code=400, detail="Invalid pet image subcategory")

    file_path = os.path.join(get_upload_subpath("pet", subcategory), filename)
    media_type, _ = mimetypes.guess_type(file_path)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, media_type=media_type or "application/octet-stream")



@router.post("/pets/{pet_id}/data", response_model=PetDataAddSchema)
async def add_pet_data(
    pet_id: int,
    pet_data: PetDataAddSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    new_data = await add_pet_data_service(pet_id, current_user["id"], pet_data, session)

    if not new_data:
        raise HTTPException(status_code=404, detail="Pet not found or data submission failed")

    return new_data



@router.patch("/pets/{pet_id}/data/edit", response_model=PetDataEditSchema)
async def edit_pet_data(
        pet_id:int,
        pet_data: PetDataEditSchema,
        session: AsyncSession = Depends(get_async_session),
        current_user: dict = Depends(get_current_user)
):
    """Edit existing pet data"""
    updated_data = await edit_pet_data_service(pet_id, current_user["id"], pet_data, session)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Pet not found or data update failed")

    return updated_data




@router.get("/pets/{pet_id}/medical_data", response_model=PetMedicalProfileShowSchema)
async def get_medical_profile_data(
    pet_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user),
):
    """Get medical profile for a specific pet"""
    pet = await get_pet_by_id(pet_id, session)

    medical_profile = await get_medical_profile_data_service(pet_id, current_user["id"], session)

    if not medical_profile:
        raise HTTPException(status_code=404, detail="Medical profile not found")

    return medical_profile



@router.post("/pets/{pet_id}/medical_data", response_model=PetMedicalProfileShowSchema)
async def add_medical_profile_data(
    pet_id: int,
    medical_data: PetMedicalProfileAddSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Add medical profile for a specific pet"""
    pet = await verify_pet_access(pet_id, current_user["id"], session)

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found or unauthorized")

    data = await prepare_medical_profile_data_service(medical_data, pet_id, current_user["id"], session)
    new_medical_data = await add_medical_profile_data_service(data, session)

    if not new_medical_data:
        raise HTTPException(status_code=500, detail="Medical profile creation failed")

    return new_medical_data



@router.patch("/pets/{pet_id}/medical_data/edit", response_model=PetMedicalProfileEditSchema)
async def edit_medical_profile_data(
    pet_id: int,
    medical_data: PetMedicalProfileEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Edit existing medical profile for a specific pet"""
    updated_medical_profile = await edit_medical_profile_data_service(pet_id, current_user["id"], medical_data, session)

    if not updated_medical_profile:
        raise HTTPException(status_code=404, detail="Medical profile not found or unauthorized")

    return updated_medical_profile



@router.post("/pets/{pet_id}/medical_data/vaccinations", response_model=PetVaccinationShowSchema)
async def add_vaccination_data(
        pet_id: int,
        vaccination_data: PetVaccinationAddSchema,
        session: AsyncSession = Depends(get_async_session),
        current_user: dict = Depends(get_current_user)
):
    """Add vaccination record for a specific pet"""
    new_vaccination_data = await add_vaccination_data_service(pet_id, vaccination_data, session, current_user["id"])

    if not new_vaccination_data:
        raise HTTPException(status_code=404, detail="Could not add vaccination data")

    return new_vaccination_data



@router.patch("/pets/{pet_id}/medical_data/vaccinations/{vaccination_id}", response_model=PetVaccinationShowSchema)
async def edit_vaccination_data(
    pet_id: int,
    vaccination_id: int,
    vaccination_data: PetVaccinationEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Edit existing vaccination record for a specific pet"""
    edited_vaccination_data = await edit_vaccination_data_service(pet_id, vaccination_id, vaccination_data, session, current_user["id"])

    if not edited_vaccination_data:
        raise HTTPException(status_code=404, detail="Vaccination record not found or unauthorized")

    return edited_vaccination_data



@router.post("/pets/{pet_id}/medical_data/medications", response_model=PetMedicationShowSchema)
async def add_medication_data(
    pet_id: int,
    medication_data: PetMedicationAddSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Add medication record for a specific pet"""
    new_medication_data = await add_medication_data_service(pet_id, medication_data, session, current_user["id"])

    if not new_medication_data:
        raise HTTPException(status_code=404, detail="Could not add medication data")

    return new_medication_data


@router.patch("/pets/{pet_id}/medical_data/medications/{medication_id}", response_model=PetMedicationShowSchema)
async def edit_medication_data(
    pet_id: int,
    medication_id: int,
    medication_data: PetMedicationEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Edit existing medication record for a specific pet"""
    edited_medication_data = await edit_medication_data_service(pet_id, medication_id, medication_data, session, current_user["id"])

    if not edited_medication_data:
        raise HTTPException(status_code=404, detail="Medication record not found or unauthorized")

    return edited_medication_data



@router.post("/pets/{pet_id}/medical_data/test_results", response_model=PetTestResultShowSchema)
async def add_test_result_data(
    pet_id: int,
    test_result_data: PetTestResultAddSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Add test result record for a specific pet"""
    new_test_result_data = await add_test_result_data_service(pet_id, test_result_data, session, current_user["id"])

    if not new_test_result_data:
        raise HTTPException(status_code=404, detail="Could not add test result data")

    return new_test_result_data


@router.patch("/pets/{pet_id}/medical_data/test_results/{test_result_id}", response_model=PetTestResultShowSchema)
async def edit_test_result_data(
    pet_id: int,
    test_result_id: int,
    test_result_data: PetTestResultEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Edit existing test result record for a specific pet"""
    edited_test_result_data = await edit_test_result_data_service(pet_id, test_result_id, test_result_data, session, current_user["id"])

    if not edited_test_result_data:
        raise HTTPException(status_code=404, detail="Test result record not found or unauthorized")

    return edited_test_result_data



@router.post("/pets/{pet_id}/medical_data/vet_visits", response_model=PetVetVisitShowSchema)
async def add_vet_visit_data(
    pet_id: int,
    vet_visit_data: PetVetVisitAddSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user),
    file: UploadFile | None = None
):
    """Add vet visit record for a specific pet"""
    new_vet_visit_data = await add_vet_visit_data_service(
        pet_id,
        vet_visit_data,
        session,
        current_user["id"],
        file
    )

    if not new_vet_visit_data:
        raise HTTPException(status_code=404, detail="Could not add vet visit data")

    return new_vet_visit_data



@router.patch("/pets/{pet_id}/medical_data/vet_visits/{vet_visit_id}", response_model=PetVetVisitShowSchema)
async def edit_vet_visit_data(
    pet_id: int,
    vet_visit_id: int,
    vet_visit_data: PetVetVisitEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user),
    file: UploadFile | None = None
):
    """Edit existing vet visit record for a specific pet"""
    updated_vet_visit = await edit_vet_visit_data_service(
        pet_id,
        vet_visit_id,
        vet_visit_data,
        session,
        current_user["id"],
        file
    )

    if not updated_vet_visit:
        raise HTTPException(status_code=404, detail="Vet visit not found or unauthorized")

    return updated_vet_visit



@router.post("/pets/{pet_id}/medical_data/documents", response_model=PetMedicalDocumentShowSchema)
async def add_medical_document_data(
    pet_id: int,
    document_name: str = Form(...),
    document_type: str = Form(...),
    upload_date: date = Form(None),
    additional_info: str = Form(None),
    file: UploadFile | None = File(None),
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Add a medical document for a specific pet"""
    document_data = PetMedicalDocumentAddSchema(
        document_name=document_name,
        document_type=document_type,
        upload_date=upload_date,
        additional_info=additional_info
    )

    result = await add_medical_document_service(
        session,
        pet_id,
        current_user["id"],
        document_data,
        file
    )

    if not result:
        raise HTTPException(status_code=404, detail="Something went wrong")

    return result



@router.patch("/pets/{pet_id}/medical_data/documents/{document_id}", response_model=PetMedicalDocumentShowSchema)
async def edit_medical_document_data(
    pet_id: int,
    document_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user),
    document_data: PetMedicalDocumentEditSchema = Depends(),
    file: UploadFile | None = File(None),
):
    """Edit an existing medical document record for a specific pet"""
    updated_document = await edit_medical_document_service(
        session,
        pet_id,
        document_id,
        current_user["id"],
        document_data,
        file
    )

    if not updated_document:
        raise HTTPException(status_code=404, detail="Medical document not found or unauthorized")

    return updated_document


