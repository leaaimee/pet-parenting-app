from fastapi import UploadFile,HTTPException

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy.orm import Session

from backend.models.pets_models import Pets
from backend.models.users_models import Users, Sitters
from backend.models.media_models import UploadedFile

from sqlalchemy.exc import SQLAlchemyError

from backend.utils.upload_helper import save_uploaded_file

from backend.schemas.pet_schema import PetProfileAddSchema, PetDataAddSchema, PetProfileEditSchema, PetDataEditSchema
from backend.schemas.pet_schema import PetMedicalProfileAddSchema, PetMedicalProfileEditSchema
from backend.schemas.pet_schema import PetVaccinationAddSchema, PetVaccinationEditSchema
from backend.schemas.pet_schema import PetMedicationAddSchema, PetMedicationEditSchema
from backend.schemas.pet_schema import PetTestResultAddSchema, PetTestResultEditSchema
from backend.schemas.pet_schema import PetVetVisitAddSchema, PetVetVisitEditSchema




from backend.models.pets_models import PetData, MedicalProfile, Medication, VaccinationRecord, TestResult, VetVisit, MedicalDocument


from backend.utils.pet_helpers import pet_birthday
from backend.services.helpers.general_helpers import apply_updates


def get_user_pets_service(user_id: int, db: Session):
    """Return all pets either owned or cared for by the user"""
    return db.query(Pets).filter(
        (Pets.parent_id == user_id) | (Pets.sitter_id == user_id)
    ).all()



def get_pet_by_id(pet_id: int, db: Session):
    return db.query(Pets).filter(Pets.id == pet_id).first()



def verify_pet_access(pet_id: int, user_id: int, db: Session):
    pet = get_pet_by_id(pet_id, db)
    if not pet or pet.parent_id != user_id:
        return None
    return pet



def view_pets_family_data_service(user_id: int, db: Session):
    pets = db.query(Pets).filter_by(parent_id=user_id).all()

    cared_for_pet_ids = (
        db.query(Sitters.pet_id)
        .filter_by(user_id=user_id)
        .distinct()
        .all()
    )
    cared_for_pet_ids = [pid[0] for pid in cared_for_pet_ids]

    cared_for_pets = db.query(Pets).filter(Pets.id.in_(cared_for_pet_ids)).all()

    return {
        "pets": pets,
        "cared_for_pets": cared_for_pets
    }


def get_pet_profile_data_service(pet_id: int, user_id: int, db: Session):
    return db.query(Pets).filter(Pets.id == pet_id, Pets.parent_id == user_id).first()




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
        "name": data.name,
        "species": data.species,
        "subspecies": data.subspecies,
        "gender": data.gender,
        "birth_year": data.birth_year,
        "birth_month": data.birth_month,
        "birthday": data.birthday,
        "profile_picture": data.profile_picture,
        "profile_description": data.profile_description,
        "parent_id": user_id
    }


def add_pet_profile_data_service(pet_data: PetProfileAddSchema, user_id: int, db: Session):
    new_pet = Pets(**pet_data.dict(), parent_id=user_id)
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet


def edit_pet_profile_data_service(
    pet_id: int,
    user_id: int,
    data: PetProfileEditSchema,
    db: Session
):
    pet = db.query(Pets).filter_by(id=pet_id, parent_id=user_id).first()

    if not pet:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(pet, field, value)

    if data.birth_year or data.birth_month or data.birthday:
        pet.birthday, pet.birth_year, pet.birth_month = pet_birthday(
            data.birth_year, data.birth_month, getattr(data, "birth_day", None)
        )

    try:
        db.commit()
        db.refresh(pet)
        return pet
    except SQLAlchemyError:
        db.rollback()
        return None


def add_pet_data_service(pet_id: int, user_id: int, data: PetDataAddSchema, db: Session):
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    new_pet_data = PetData(pet_id=pet_id, user_id=user_id, **data.dict())
    db.add(new_pet_data)
    db.commit()
    db.refresh(new_pet_data)
    return new_pet_data


def edit_pet_data_service(pet_id: int, user_id: int, data: PetDataEditSchema, db: Session):
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    pet_data = db.query(PetData).filter_by(pet_id=pet_id).first()
    if not pet_data:
        pet_data = PetData(pet_id=pet_id, user_id=user_id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(pet_data, field, value or "")
    # TODO: Replace setattr loop with apply_updates helper when fresh

    db.add(pet_data)
    db.commit()
    db.refresh(pet_data)
    return pet_data


def get_medical_profile_data_service(pet_id: int, user_id: int, db: Session):
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    return db.query(MedicalProfile).filter_by(pet_id=pet_id).first()


def prepare_medical_profile_data_service(
    data: PetMedicalProfileAddSchema,
    pet_id: int,
    user_id: int,
    db: Session
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


def add_medical_profile_data_service(data: dict, db: Session):
    new_medical_profile = MedicalProfile(**data)
    db.add(new_medical_profile)
    db.commit()
    db.refresh(new_medical_profile)
    return new_medical_profile


def edit_medical_profile_data_service(
    pet_id: int,
    user_id: int,
    data: PetMedicalProfileEditSchema,
    db: Session
):
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    medical_profile = db.query(MedicalProfile).filter_by(pet_id=pet_id).first()
    if not medical_profile:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(medical_profile, field, value or "")
    # TODO: Replace setattr loop with apply_updates helper when fresh
    db.commit()
    db.refresh(medical_profile)
    return medical_profile




def add_vaccination_data_service(
    pet_id: int,
    vaccination_data: PetVaccinationAddSchema,
    db: Session,
    user_id: int
):
    """Create a new vaccination record for a specific pet"""
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    medical_profile = db.query(MedicalProfile).filter_by(pet_id=pet_id).first()
    if not medical_profile:
        return None

    new_vaccination = VaccinationRecord(
        medical_profile_id=medical_profile.id,
        pet_id=pet_id,
        **vaccination_data.dict()
    )


    db.add(new_vaccination)
    db.commit()
    db.refresh(new_vaccination)
    return new_vaccination



def edit_vaccination_data_service(
    pet_id: int,
    vaccination_id: int,
    vaccination_data: PetVaccinationEditSchema,
    db: Session,
    user_id: int
):
    """Edit an existing vaccination record for a specific pet"""
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    record = db.query(VaccinationRecord).filter_by(id=vaccination_id, pet_id=pet_id).first()
    if not record:
        return None

    for field, value in vaccination_data.dict(exclude_unset=True).items():
        setattr(record, field, value or "")
    # TODO: Replace setattr loop with apply_updates helper when fresh
    db.commit()
    db.refresh(record)
    return record



def add_medication_data_service(
    pet_id: int,
    medication_data: PetMedicationAddSchema,
    db: Session,
    user_id: int
):
    """Create and store a new medication record linked to the pet's medical profile"""
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    medical_profile = db.query(MedicalProfile).filter_by(pet_id=pet_id).first()
    if not medical_profile:
        return None

    new_medication = Medication(
        medical_profile_id=medical_profile.id,
        pet_id=pet_id,
        **medication_data.dict(exclude_unset=True)
    )

    db.add(new_medication)
    db.commit()
    db.refresh(new_medication)
    return new_medication


def edit_medication_data_service(
    pet_id: int,
    medication_id: int,
    medication_data: PetMedicationEditSchema,
    db: Session,
    user_id: int
):
    """Edit an existing medication record for a specific pet"""
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    record = db.query(Medication).filter_by(id=medication_id, pet_id=pet_id).first()
    if not record:
        return None

    for field, value in medication_data.dict(exclude_unset=True).items():
        setattr(record, field, value if value is not None else "")
    # TODO: Replace setattr loop with apply_updates helper when fresh
    db.commit()
    db.refresh(record)
    return record



def add_test_result_data_service(
    pet_id: int,
    test_result_data: PetTestResultAddSchema,
    db: Session,
    user_id: int
):
    """Create a new test result record for a specific pet"""
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    medical_profile = db.query(MedicalProfile).filter_by(pet_id=pet_id).first()
    if not medical_profile:
        return None

    # Only include fields that match the model
    allowed_fields = ['test_type', 'result', 'date', 'additional_info']
    fields = {
        k: v for k, v in test_result_data.dict(exclude_unset=True).items() if k in allowed_fields
    }

    new_test_result = TestResult(
        medical_profile_id=medical_profile.id,
        pet_id=pet_id,
        **fields
    )

    db.add(new_test_result)
    db.commit()
    db.refresh(new_test_result)
    return new_test_result


def edit_test_result_data_service(
    pet_id: int,
    test_result_id: int,
    test_result_data: PetTestResultEditSchema,
    db: Session,
    user_id: int
):
    """Edit an existing test result record for a specific pet"""

    # 1. Verify access
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    # 2. Get the correct test result record
    record = db.query(TestResult).filter_by(id=test_result_id, pet_id=pet_id).first()
    if not record:
        return None

    # 3. Apply updates using centralized helper
    apply_updates(
        record,
        test_result_data.dict(exclude_unset=True),
        empty_string_fields={"result", "additional_info"}  # only fill with "" if needed
    )

    # 4. Save to DB
    db.commit()
    db.refresh(record)
    return record



def add_vet_visit_data_service(
    pet_id: int,
    vet_visit_data: PetVetVisitAddSchema,
    db: Session,
    user_id: int,
    file: UploadFile | None = None
):
    """Create a new vet visit record for a specific pet"""
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    medical_profile = db.query(MedicalProfile).filter_by(pet_id=pet_id).first()
    if not medical_profile:
        return None

    filename = ""
    if file:
        filename = save_uploaded_file(file, category="medical", subcategory="xray")

    fields = {
        k: v for k, v in vet_visit_data.dict(exclude_unset=True).items()
        if k in ["reason", "vet_name", "clinic_info", "date"]
    }

    new_vet_visit = VetVisit(
        medical_profile_id=medical_profile.id,
        pet_id=pet_id,
        documents=filename or "",
        **fields
    )

    db.add(new_vet_visit)
    db.commit()
    db.refresh(new_vet_visit)
    return new_vet_visit


def edit_vet_visit_data_service(
    pet_id: int,
    vet_visit_id: int,
    vet_visit_data: PetVetVisitEditSchema,
    db: Session,
    user_id: int,
    file: UploadFile | None = None
):
    """Edit an existing vet visit record for a specific pet"""
    pet = verify_pet_access(pet_id, user_id, db)
    if not pet:
        return None

    record = db.query(VetVisit).filter_by(id=vet_visit_id, pet_id=pet_id).first()
    if not record:
        return None

    # Handle optional file upload
    if file:
        filename = save_uploaded_file(file, category="medical", subcategory="xray")
        vet_visit_data.documents = filename

    # Apply updates using helper
    allowed_fields = {"reason", "vet_name", "clinic_info", "date", "documents"}
    data_dict = vet_visit_data.dict(exclude_unset=True)
    apply_updates(record, data_dict, empty_string_fields=allowed_fields)

    db.commit()
    db.refresh(record)
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




def add_medical_document_data_service()


def edit_medical_document_data_service()




