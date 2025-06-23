from datetime import date

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user

from backend.database import get_async_session

from backend.auth.auth2 import get_current_user

from backend.models.users_models import Users

from backend.schemas.medical_schema import PetMedicalProfileShowSchema, PetMedicalProfileAddSchema, \
    PetMedicalProfileEditSchema, PetVaccinationShowSchema, PetVaccinationAddSchema, PetVaccinationEditSchema, \
    PetMedicationShowSchema, PetMedicationAddSchema, PetMedicationEditSchema, PetTestResultShowSchema, \
    PetTestResultAddSchema, PetTestResultEditSchema, PetMedicalDocumentShowSchema, PetMedicalDocumentAddSchema, \
    PetMedicalDocumentEditSchema, PetVetVisitShowSchema, PetVetVisitAddSchema, PetVetVisitEditSchema
from backend.services.pets_service import verify_pet_access
from backend.services.medical_service import get_medical_profile_service, prepare_medical_profile_service, \
    add_medical_profile_service, edit_medical_profile_service, add_vaccination_data_service, \
    edit_vaccination_data_service, add_medication_data_service, edit_medication_data_service, \
    add_test_result_data_service, edit_test_result_data_service, add_vet_visit_data_service, \
    edit_vet_visit_data_service, add_medical_document_service, edit_medical_document_service, \
    show_vaccination_data_service, show_medication_data_service

from backend.domain.exceptions import NotFoundError

router = APIRouter()

@router.get("/pets/{pet_id}/medical_data", response_model=PetMedicalProfileShowSchema)
async def get_medical_profile_data(
    pet_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user)
):
    """Get medical profile for a specific pet"""
    medical_profile = await get_medical_profile_service(pet_id, current_user.id, session)
    if not medical_profile:
        raise NotFoundError("Medical profile not found")
    return medical_profile


@router.post("/pets/{pet_id}/medical_data", response_model=PetMedicalProfileShowSchema)
async def add_medical_profile_data(
    pet_id: int,
    medical_data: PetMedicalProfileAddSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user)
):
    """Add medical profile for a specific pet"""
    await verify_pet_access(pet_id, current_user.id, session)
    data = prepare_medical_profile_service(medical_data, pet_id)
    return await add_medical_profile_service(data, session)


@router.patch("/pets/{pet_id}/medical_data/edit", response_model=PetMedicalProfileEditSchema)
async def edit_medical_profile_data(
    pet_id: int,
    medical_data: PetMedicalProfileEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user)
):
    """Edit existing medical profile for a specific pet"""
    updated = await edit_medical_profile_service(
        pet_id, current_user.id, medical_data, session
    )
    if not updated:
        raise NotFoundError("Medical profile not found or unauthorized")
    return updated


@router.get("pets/{pet_id}/medical_data/vaccinations", response_model=PetVaccinationShowSchema)
async def show_vaccination_data(
        pet_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: Users = Depends(get_current_user)
):
    """Show vaccination data for a specific pet"""
    vaccination_data = await show_vaccination_data_service(pet_id, current_user.id, session)
    if not vaccination_data:
        raise NotFoundError("Vaccination data not found")
    return vaccination_data


@router.post("/pets/{pet_id}/medical_data/vaccinations", response_model=PetVaccinationShowSchema)
async def add_vaccination_data(
        pet_id: int,
        vaccination_data: PetVaccinationAddSchema,
        session: AsyncSession = Depends(get_async_session),
        current_user: Users = Depends(get_current_user)
):
    """Add vaccination record for a specific pet"""
    new_vaccination_data = await add_vaccination_data_service(pet_id, vaccination_data, session, current_user.id)

    if not new_vaccination_data:
        raise NotFoundError("Could not add vaccination data")

    return new_vaccination_data


@router.patch("/pets/{pet_id}/medical_data/vaccinations/{vaccination_id}", response_model=PetVaccinationShowSchema)
async def edit_vaccination_data(
    pet_id: int,
    vaccination_id: int,
    vaccination_data: PetVaccinationEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user)
):
    """Edit existing vaccination record for a specific pet"""
    edited_vaccination_data = await edit_vaccination_data_service(pet_id, vaccination_id, vaccination_data, session, current_user.id)

    if not edited_vaccination_data:
        raise NotFoundError("Vaccination record not found or unauthorized")

    return edited_vaccination_data


@router.get("/pets/{pet_id}/medical_data/medications", response_model=PetMedicationShowSchema)
async def show_medication_data(
        pet_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: Users = Depends(get_current_user)
):
    """Display medication record for a specific pet"""
    medication_data = await show_medication_data_service(pet_id, session, current_user.id)

    if not medication_data:
        raise NotFoundError("Medication data not found")

    return medication_data



@router.post("/pets/{pet_id}/medical_data/medications", response_model=PetMedicationShowSchema)
async def add_medication_data(
    pet_id: int,
    medication_data: PetMedicationAddSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Add medication record for a specific pet"""
    new_medication_data = await add_medication_data_service(pet_id, medication_data, session, current_user.id)

    if not new_medication_data:
        raise NotFoundError("Could not add medication data")

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
    edited_medication_data = await edit_medication_data_service(pet_id, medication_id, medication_data, session, current_user.id)

    if not edited_medication_data:
        raise NotFoundError("Medication record not found or unauthorized")

    return edited_medication_data


@router.post("/pets/{pet_id}/medical_data/test_results", response_model=PetTestResultShowSchema)
async def add_test_result_data(
    pet_id: int,
    test_result_data: PetTestResultAddSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Add test result record for a specific pet"""
    new_test_result_data = await add_test_result_data_service(pet_id, test_result_data, session, current_user.id)

    if not new_test_result_data:
        raise NotFoundError("Could not add test result data")

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
    edited_test_result_data = await edit_test_result_data_service(pet_id, test_result_id, test_result_data, session, current_user.id)

    if not edited_test_result_data:
        raise NotFoundError("Test result record not found or unauthorized")

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
        current_user.id,
        file
    )

    if not new_vet_visit_data:
        raise NotFoundError("Could not add vet visit data")

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
        current_user.id,
        file
    )

    if not updated_vet_visit:
        raise NotFoundError("Vet visit not found or unauthorized")

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
