from fastapi import UploadFile,HTTPException

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.models.pets_models import Pets
from backend.models.users_models import Users, Sitters
from backend.models.media_models import UploadedFile

from backend.utils.upload_helper import save_uploaded_file

from backend.schemas.pet_schema import PetProfileAddSchema, PetDataAddSchema, PetProfileEditSchema, PetDataEditSchema
from backend.schemas.pet_schema import PetMedicalProfileAddSchema, PetMedicalProfileEditSchema
from backend.schemas.pet_schema import PetVaccinationAddSchema, PetVaccinationEditSchema
from backend.schemas.pet_schema import PetMedicationAddSchema, PetMedicationEditSchema
from backend.schemas.pet_schema import PetTestResultAddSchema, PetTestResultEditSchema
from backend.schemas.pet_schema import PetVetVisitAddSchema, PetVetVisitEditSchema
from backend.schemas.pet_schema import PetMedicalDocumentShowSchema, PetMedicalDocumentAddSchema, PetMedicalDocumentEditSchema


from backend.models.pets_models import PetData, MedicalProfile, Medication, VaccinationRecord, TestResult, VetVisit, MedicalDocument

from backend.utils.pet_helpers import pet_birthday
from backend.services.helpers.general_helpers import apply_updates


async def get_user_pets_service(user_id: int, session: AsyncSession):
    result = await session.execute(
        select(Pets).where(
            (Pets.parent_id == user_id) | (Pets.sitter_id == user_id)
        )
    )
    return result.scalars().all()




async def get_pet_by_id(pet_id: int, session: AsyncSession):
    result = await session.execute(
        select(Pets).where(Pets.id == pet_id)
    )
    return result.scalar_one_or_none()



async def verify_pet_access(pet_id: int, user_id: int, session: AsyncSession):
    pet = await get_pet_by_id(pet_id, session)
    if not pet or pet.parent_id != user_id:
        return None
    return pet



async def view_pets_family_data_service(user_id: int, session: AsyncSession):
    pets_result = await session.execute(select(Pets).filter_by(parent_id=user_id))
    pets = pets_result.scalars().all()

    sitter_result = await session.execute(
        select(Sitters.pet_id).filter_by(user_id=user_id).distinct()
    )
    cared_for_pet_ids = [row[0] for row in sitter_result.all()]

    if cared_for_pet_ids:
        cared_for_result = await session.execute(
            select(Pets).filter(Pets.id.in_(cared_for_pet_ids))
        )
        cared_for_pets = cared_for_result.scalars().all()
    else:
        cared_for_pets = []

    return {
        "pets": pets,
        "cared_for_pets": cared_for_pets
    }


async def get_pet_profile_data_service(pet_id: int, user_id: int, session: AsyncSession):
    result = await session.execute(
        select(Pets).where(Pets.id == pet_id, Pets.parent_id == user_id)
    )
    return result.scalar_one_or_none()




async def add_pet_profile_image_service(
    session: AsyncSession,
    file: UploadFile,
    pet_id: int
) -> UploadedFile:
    # Step 1: Save file to disk & get metadata
    file_info = await save_uploaded_file(file, category="pet", subcategory="profile_pic")
    file_hash: str = file_info["file_hash"]

    # Step 2: Deduplication check
    existing = await session.execute(
        select(UploadedFile).where(UploadedFile.file_hash == file_hash)
    )
    existing_file = existing.scalar_one_or_none()

    if existing_file:
        # Step 3: Reassign pet_id if needed
        if existing_file.pet_id != pet_id:
            existing_file.pet_id = pet_id
            await session.commit()
        return existing_file

    # Step 4: Create new file entry
    new_file = UploadedFile(
        **file_info,
        pet_id=pet_id,
        upload_time=datetime.utcnow()
    )
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)

    return new_file



def prepare_pet_profile_data(data: PetProfileAddSchema, user_id: int) -> dict:
    return {
        **data.dict(exclude_unset=True),
        "parent_id": user_id
    }


async def add_pet_profile_data_service(pet_data: PetProfileAddSchema, user_id: int, session: AsyncSession):
    new_pet = Pets(**pet_data.dict(exclude_unset=True), parent_id=user_id)
    session.add(new_pet)
    await session.commit()
    await session.refresh(new_pet)
    return new_pet



async def edit_pet_profile_data_service(
    pet_id: int,
    user_id: int,
    data: PetProfileEditSchema,
    session: AsyncSession
):
    result = await session.execute(
        select(Pets).where(Pets.id == pet_id, Pets.parent_id == user_id)
    )
    pet = result.scalar_one_or_none()

    if not pet:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(pet, field, value)

    if data.birth_year or data.birth_month or data.birthday:
        pet.birthday, pet.birth_year, pet.birth_month = pet_birthday(
            data.birth_year, data.birth_month, getattr(data, "birth_day", None)
        )

    try:
        await session.commit()
        await session.refresh(pet)
        return pet
    except SQLAlchemyError:
        await session.rollback()
        return None



async def add_pet_data_service(
    pet_id: int,
    user_id: int,
    data: PetDataAddSchema,
    session: AsyncSession
):
    result = await session.execute(
        select(Pets).where(Pets.id == pet_id, Pets.parent_id == user_id)
    )
    pet = result.scalar_one_or_none()

    if not pet:
        return None

    new_pet_data = PetData(pet_id=pet_id, user_id=user_id, **data.dict())
    session.add(new_pet_data)
    await session.commit()
    await session.refresh(new_pet_data)

    return new_pet_data



async def edit_pet_data_service(
    pet_id: int,
    user_id: int,
    data: PetDataEditSchema,
    session: AsyncSession
):
    result = await session.execute(
        select(Pets).where(Pets.id == pet_id, Pets.parent_id == user_id)
    )
    pet = result.scalar_one_or_none()
    if not pet:
        return None

    result = await session.execute(
        select(PetData).where(PetData.pet_id == pet_id)
    )
    pet_data = result.scalar_one_or_none()

    if not pet_data:
        pet_data = PetData(pet_id=pet_id, user_id=user_id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(pet_data, field, value or "")
        # TODO: Replace setattr loop with apply_updates helper when fresh

    session.add(pet_data)
    await session.commit()
    await session.refresh(pet_data)
    return pet_data



async def get_medical_profile_data_service(pet_id: int, user_id: int, session: AsyncSession):
    pet = await verify_pet_access(pet_id, user_id, session)
    if not pet:
        return None

    result = await session.execute(
        select(MedicalProfile).where(MedicalProfile.pet_id == pet_id)
    )
    return result.scalar_one_or_none()



def prepare_medical_profile_data_service(
    data: PetMedicalProfileAddSchema,
    pet_id: int
) -> dict:
    """Prepare medical profile data for creation"""
    return {
        "pet_id": pet_id,
        "blood_type": data.blood_type,
        "weight": data.weight,
        "weight_updated": data.weight_updated,
        "chronic_conditions": data.chronic_conditions,
        "notes": data.notes
    }



async def add_medical_profile_data_service(data: dict, session: AsyncSession):
    new_medical_profile = MedicalProfile(**data)
    session.add(new_medical_profile)
    await session.commit()
    await session.refresh(new_medical_profile)
    return new_medical_profile



async def edit_medical_profile_data_service(
    session: AsyncSession,
    pet_id: int,
    user_id: int,
    data: PetMedicalProfileEditSchema
):
    pet = await verify_pet_access(pet_id, user_id, session)
    if not pet:
        return None

    result = await session.execute(
        select(MedicalProfile).where(MedicalProfile.pet_id == pet_id)
    )
    medical_profile = result.scalar_one_or_none()
    if not medical_profile:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(medical_profile, field, value)

    await session.commit()
    await session.refresh(medical_profile)
    return medical_profile



async def add_vaccination_data_service(
    pet_id: int,
    vaccination_data: PetVaccinationAddSchema,
    session: AsyncSession,
    user_id: int
):
    """Create a new vaccination record for a specific pet"""
    pet = await verify_pet_access(pet_id, user_id, session)
    if not pet:
        return None

    result = await session.execute(
        select(MedicalProfile).where(MedicalProfile.pet_id == pet_id)
    )
    medical_profile = result.scalar_one_or_none()
    if not medical_profile:
        return None

    new_vaccination = VaccinationRecord(
        medical_profile_id=medical_profile.id,
        pet_id=pet_id,
        **vaccination_data.dict()
    )

    session.add(new_vaccination)
    await session.commit()
    await session.refresh(new_vaccination)
    return new_vaccination




async def edit_vaccination_data_service(
    pet_id: int,
    vaccination_id: int,
    vaccination_data: PetVaccinationEditSchema,
    session: AsyncSession,
    user_id: int
):
    """Edit an existing vaccination record for a specific pet"""
    pet = await verify_pet_access(pet_id, user_id, session)
    if not pet:
        return None

    result = await session.execute(
        select(VaccinationRecord).where(
            VaccinationRecord.id == vaccination_id,
            VaccinationRecord.pet_id == pet_id
        )
    )
    record = result.scalar_one_or_none()
    if not record:
        return None

    for field, value in vaccination_data.dict(exclude_unset=True).items():
        setattr(record, field, value or "")
    # TODO: Replace setattr loop with apply_updates helper when fresh

    await session.commit()
    await session.refresh(record)
    return record




async def add_medication_data_service(
    pet_id: int,
    medication_data: PetMedicationAddSchema,
    session: AsyncSession,
    user_id: int
):
    """Create and store a new medication record linked to the pet's medical profile"""
    pet = await verify_pet_access(pet_id, user_id, session)
    if not pet:
        return None

    result = await session.execute(
        select(MedicalProfile).where(MedicalProfile.pet_id == pet_id)
    )
    medical_profile = result.scalar_one_or_none()
    if not medical_profile:
        return None

    new_medication = Medication(
        medical_profile_id=medical_profile.id,
        pet_id=pet_id,
        **medication_data.dict(exclude_unset=True)
    )

    session.add(new_medication)
    await session.commit()
    await session.refresh(new_medication)
    return new_medication



async def edit_medication_data_service(
    pet_id: int,
    medication_id: int,
    medication_data: PetMedicationEditSchema,
    session: AsyncSession,
    user_id: int
):
    """Edit an existing medication record for a specific pet"""
    pet = await verify_pet_access(pet_id, user_id, session)
    if not pet:
        return None

    result = await session.execute(
        select(Medication).where(Medication.id == medication_id, Medication.pet_id == pet_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        return None

    for field, value in medication_data.dict(exclude_unset=True).items():
        setattr(record, field, value if value is not None else "")

    await session.commit()
    await session.refresh(record)
    return record




async def add_test_result_data_service(
    pet_id: int,
    test_result_data: PetTestResultAddSchema,
    session: AsyncSession,
    user_id: int
):
    """Create a new test result record for a specific pet"""
    pet = await verify_pet_access(pet_id, user_id, session)
    if not pet:
        return None

    result = await session.execute(
        select(MedicalProfile).where(MedicalProfile.pet_id == pet_id)
    )
    medical_profile = result.scalar_one_or_none()
    if not medical_profile:
        return None

    # Only include fields that match the model
    allowed_fields = ["test_type", "result", "date", "additional_info"]
    fields = {
        k: v for k, v in test_result_data.dict(exclude_unset=True).items() if k in allowed_fields
    }

    new_test_result = TestResult(
        medical_profile_id=medical_profile.id,
        pet_id=pet_id,
        **fields
    )

    session.add(new_test_result)
    await session.commit()
    await session.refresh(new_test_result)
    return new_test_result



async def edit_test_result_data_service(
    pet_id: int,
    test_result_id: int,
    test_result_data: PetTestResultEditSchema,
    session: AsyncSession,
    user_id: int
):
    """Edit an existing test result record for a specific pet"""

    # 1. Verify access
    pet = await verify_pet_access(pet_id, user_id, session)
    if not pet:
        return None

    # 2. Get the correct test result record
    result = await session.execute(
        select(TestResult).where(TestResult.id == test_result_id, TestResult.pet_id == pet_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        return None

    # 3. Apply updates using centralized helper
    apply_updates(
        record,
        test_result_data.dict(exclude_unset=True),
        empty_string_fields={"result", "additional_info"}
    )

    # 4. Save to DB
    await session.commit()
    await session.refresh(record)
    return record




async def add_vet_visit_data_service(
    pet_id: int,
    vet_visit_data: PetVetVisitAddSchema,
    session: AsyncSession,
    user_id: int,
    file: UploadFile | None = None
):
    """Create a new vet visit record for a specific pet"""
    pet = await verify_pet_access(pet_id, user_id, session)
    if not pet:
        return None

    result = await session.execute(
        select(MedicalProfile).where(MedicalProfile.pet_id == pet_id)
    )
    medical_profile = result.scalar_one_or_none()
    if not medical_profile:
        return None

    filename = ""
    if file:
        file_info = await save_uploaded_file(file, category="medical", subcategory="xray")
        filename = file_info["filepath"]

    fields = {
        k: v for k, v in vet_visit_data.dict(exclude_unset=True).items()
        if k in {"reason", "vet_name", "clinic_info", "date"}
    }

    new_vet_visit = VetVisit(
        medical_profile_id=medical_profile.id,
        pet_id=pet_id,
        documents=filename or "",
        **fields
    )

    session.add(new_vet_visit)
    await session.commit()
    await session.refresh(new_vet_visit)
    return new_vet_visit



async def edit_vet_visit_data_service(
    pet_id: int,
    vet_visit_id: int,
    vet_visit_data: PetVetVisitEditSchema,
    session: AsyncSession,
    user_id: int,
    file: UploadFile | None = None
):
    """Edit an existing vet visit record for a specific pet"""
    pet = await verify_pet_access(pet_id, user_id, session)
    if not pet:
        return None

    result = await session.execute(
        select(VetVisit).where(VetVisit.id == vet_visit_id, VetVisit.pet_id == pet_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        return None

    # Handle optional file upload
    if file:
        file_info = await save_uploaded_file(file, category="medical", subcategory="xray")
        vet_visit_data.documents = file_info["filepath"]

    # Apply updates using helper
    allowed_fields = {"reason", "vet_name", "clinic_info", "date", "documents"}
    data_dict = vet_visit_data.dict(exclude_unset=True)
    apply_updates(record, data_dict, empty_string_fields=allowed_fields)

    await session.commit()
    await session.refresh(record)
    return record




async def link_document_to_vet_visit_service(
    session: AsyncSession,
    document_id: int,
    vet_visit_id: int
) -> MedicalDocument:
    doc = await session.get(MedicalDocument, document_id)
    visit = await session.get(VetVisit, vet_visit_id)

    if not doc or not visit:
        raise HTTPException(status_code=404, detail="Document or Vet Visit not found")

    doc.vet_visit_id = vet_visit_id
    await session.commit()
    await session.refresh(doc)
    return doc




async def add_medical_document_service(
    session: AsyncSession,
    pet_id: int,
    user_id: int,
    document_data: PetMedicalDocumentAddSchema,  # ✅ write schema
    file: UploadFile | None = None
):
    """Create a new medical document record for a specific pet."""

    if not user_id:
        raise HTTPException(status_code=401, detail="User authentication required")

    pet = await verify_pet_access(pet_id, user_id, session)  # ✅ async
    if not pet:
        raise HTTPException(status_code=403, detail="Access denied to this pet")

    if not file:
        raise HTTPException(status_code=400, detail="File is required for medical documents")

    file_info = await save_uploaded_file(file, category="medical", subcategory="documents")  # ✅ async
    file_hash = file_info["file_hash"]

    result = await session.execute(
        select(MedicalDocument).where(MedicalDocument.file_hash == file_hash)
    )
    existing_document = result.scalar_one_or_none()

    if existing_document:
        return existing_document

    new_document = MedicalDocument(
        pet_id=pet_id,
        user_id=user_id,
        file_hash=file_hash,
        upload_time=datetime.utcnow(),
        **document_data.dict(exclude_unset=True),
    )

    session.add(new_document)
    await session.commit()
    await session.refresh(new_document)
    return new_document




async def edit_medical_document_service(
    session: AsyncSession,
    pet_id: int,
    document_id: int,
    user_id: int,
    document_data: PetMedicalDocumentEditSchema,
    file: UploadFile | None = None,
):
    """Edit an existing medical document's metadata"""

    # Get the document
    document = await session.get(MedicalDocument, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Medical document not found")

    # Ensure the user has access
    pet = await verify_pet_access(document.pet_id, user_id, session)
    if not pet:
        raise HTTPException(status_code=403, detail="Access denied to this pet")

    # Update fields from the schema
    for field, value in document_data.dict(exclude_unset=True).items():
        setattr(document, field, value)

    await session.commit()
    await session.refresh(document)
    return document

