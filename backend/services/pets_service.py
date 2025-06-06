from fastapi import UploadFile, HTTPException


from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from backend.models.pets_models import Pets
from backend.models.medical_models import MedicalProfile, VaccinationRecord, VetVisit, MedicalDocument
from backend.models.users_models import Sitters
from backend.models.media_models import UploadedFile

from backend.utils.upload_helper import save_uploaded_file

from backend.schemas.pet_schema import PetProfileAddSchema, PetDataAddSchema, PetProfileEditSchema, PetDataEditSchema

from backend.models.pets_models import PetData

from backend.utils.pet_helpers import pet_birthday




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




def is_pet_data_empty(data: PetData) -> bool:
    return all([
        not data.favorite_things,
        not data.dislikes,
        not data.social_style,
        not data.communication,
        not data.preferred_treats,
        not data.diet,
        not data.allergies,
        not data.medical_alerts,
        not data.behavior_notes,
        not data.additional_info
    ])


def is_pet_profile_empty(data: Pets) -> bool:
    return all([
        not data.birthday,
        not data.birth_year,
        not data.birth_month,
        not data.subspecies,
        not data.gender,
        not data.profile_image_id,
        not data.profile_description or data.profile_description.strip() == ""
    ])



async def delete_pet_profile_service(pet_id: int, user_id: int, session: AsyncSession):
    try:
        # Get pet
        pet_result = await session.execute(
            select(Pets).where(Pets.id == pet_id)
        )
        pet = pet_result.scalar_one_or_none()

        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found")

        if pet.parent_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this pet")

        # Check if pet data exists
        data_result = await session.execute(
            select(PetData).where(PetData.pet_id == pet_id)
        )
        pet_data = data_result.scalar_one_or_none()

        if pet_data and not is_pet_data_empty(pet_data):
            raise HTTPException(status_code=400, detail="Cannot delete pet — PetData is not empty")

        # Check if pet profile has meaningful fields
        if not is_pet_profile_empty(pet):
            raise HTTPException(status_code=400, detail="Cannot delete pet — Profile still contains information")

        # Auto-delete medical sub-records
        for model in [VetVisit, VaccinationRecord, MedicalDocument]:
            result = await session.execute(
                select(model).where(model.pet_id == pet_id)
            )
            entries = result.scalars().all()
            for entry in entries:
                await session.delete(entry)

        # Delete medical profile if exists
        med_result = await session.execute(
            select(MedicalProfile).where(MedicalProfile.pet_id == pet_id)
        )
        med_profile = med_result.scalar_one_or_none()
        if med_profile:
            await session.delete(med_profile)

        # Delete PetData if exists
        if pet_data:
            await session.delete(pet_data)

        # Delete Pet itself
        await session.delete(pet)
        await session.commit()

        return {"detail": "Pet and related data deleted successfully"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete pet: {str(e)}")



async def delete_pet_data_service(pet_id: int, user_id: int, session: AsyncSession):
    try:
        # Verify ownership
        pet_result = await session.execute(
            select(Pets).where(Pets.id == pet_id)
        )
        pet = pet_result.scalar_one_or_none()

        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found")

        if pet.parent_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this pet")

        # Get PetData
        data_result = await session.execute(
            select(PetData).where(PetData.pet_id == pet_id)
        )
        pet_data = data_result.scalar_one_or_none()

        if not pet_data:
            raise HTTPException(status_code=404, detail="Pet data not found")

        await session.delete(pet_data)
        await session.commit()
        return {"detail": "Pet data deleted successfully"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete pet data: {str(e)}")
