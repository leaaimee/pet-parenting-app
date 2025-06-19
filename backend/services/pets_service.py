from datetime import datetime

from fastapi import UploadFile

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from backend.models.media_models import ProfileUpload
from backend.models.pets_models import Pets
from backend.models.medical_models import MedicalProfile, VaccinationRecord, VetVisit, MedicalDocument

from datetime import date
from typing import Optional, Tuple

from backend.utils.upload_helper import save_uploaded_file

from backend.schemas.pet_schema import PetProfileAddSchema, PetDataAddSchema, PetProfileEditSchema, PetDataEditSchema

from backend.models.pets_models import PetData

from backend.utils.pet_helpers import pet_birthday

from backend.domain.exceptions import NotFoundError, InternalError, PermissionDeniedError, ConflictError


async def get_user_pets_service(user_id: int, session: AsyncSession):
    result = await session.execute(
        select(Pets).where(Pets.parent_id == user_id)
    )
    return result.scalars().all()



def pet_birthday(
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[date] = None,
) -> Tuple[Optional[date], Optional[int], Optional[int]]:
    """
    Normalize the pet’s birthday information into:
      (birthday: date | None,
       birth_year: int    | None,
       birth_month: int   | None)

    - If `day` is provided (a full date), we extract year/month/day.
    - Else if only `year` + `month` are provided, we pick the 1st of that month.
    - Else if only `year` is provided, we default to January 1st of that year.
    - Otherwise, we return (None, None, None).
    """
    if day:
        # Full date given
        return day, day.year, day.month

    if year and month:
        # Year + month known, approximate to first day of month
        try:
            approx = date(year, month, 1)
            return approx, year, month
        except ValueError:
            # Bad month (e.g. month=13)? Fall back to January 1st
            approx = date(year, 1, 1)
            return approx, year, 1

    if year:
        # Only year known, approximate to January 1st
        approx = date(year, 1, 1)
        return approx, year, 1

    # Nothing known
    return None, None, None



async def get_pet_profile_service(
    pet_id: int,
    owner_id: int,
    session: AsyncSession
) -> Pets:
    result = await session.execute(
        select(Pets)
        .options(
            selectinload(Pets.pet_data),
            selectinload(Pets.profile_uploads),
        )
        .where(Pets.id == pet_id, Pets.parent_id == owner_id)
    )
    pet = result.scalar_one_or_none()
    if not pet:
        raise NotFoundError("Pet not found or access denied.")
    return pet



async def add_pet_profile_service(
    pet_data: PetProfileAddSchema,
    owner_id: int,
    session: AsyncSession,
) -> Pets:
    # 1) Extract the raw values from the schema
    raw = pet_data.model_dump(
        mode="python",
        exclude_unset=True,
        exclude_none=True,
    )

    # 2) Normalize birthday/year/month
    bday, byear, bmonth = pet_birthday(
        year=raw.get("birth_year"),
        month=raw.get("birth_month"),
        day=raw.get("birthday"),
    )

    # 3) Build the kwargs for Pets, dropping the raw keys
    pet_kwargs = {
        k: v for k, v in raw.items()
        if k not in ("birth_year", "birth_month", "birthday")
    }
    pet_kwargs.update({
        "birthday":    bday,
        "birth_year":  byear,
        "birth_month": bmonth,
        "parent_id":   owner_id,
    })

    # 4) Create & persist
    new_pet = Pets(**pet_kwargs)
    session.add(new_pet)
    try:
        await session.commit()
        await session.refresh(new_pet)
        return new_pet
    except SQLAlchemyError:
        await session.rollback()
        raise InternalError("Failed to create pet. Please try again.")



async def edit_pet_profile_service(
    pet_id: int,
    owner_id: int,
    data: PetProfileEditSchema,
    session: AsyncSession,
) -> Pets:
    # 1) Load & authorize
    pet = await get_pet_profile_service(pet_id, owner_id, session)

    # 2) Extract only what the client sent
    raw = data.model_dump(
        mode="python",
        exclude_unset=True,
        exclude_none=True,
    )

    # 3) Normalize birthday/year/month if any changed
    if any(key in raw for key in ("birthday", "birth_year", "birth_month")):
        bday, byear, bmonth = pet_birthday(
            year=raw.get("birth_year"),
            month=raw.get("birth_month"),
            day=raw.get("birthday"),
        )
        # Overwrite those three in the raw dict
        raw.update({
            "birthday":    bday,
            "birth_year":  byear,
            "birth_month": bmonth,
        })

    # 4) Apply every other field
    for field, value in raw.items():
        if field not in ("birthday", "birth_year", "birth_month"):
            setattr(pet, field, value)
    # Finally set the normalized date fields
    pet.birthday   = raw["birthday"]
    pet.birth_year = raw["birth_year"]
    pet.birth_month= raw["birth_month"]

    # 5) Commit & return
    try:
        await session.commit()
        await session.refresh(pet)
        return pet
    except SQLAlchemyError:
        await session.rollback()
        raise InternalError("Failed to update pet. Please try again.")



async def add_pet_profile_image_service(
    session: AsyncSession,
    file: UploadFile,
    pet_id: int,
    user_id: int,
) -> ProfileUpload:                                  # ← annotate with ProfileUpload
    # Step 1: Save to disk
    file_info = await save_uploaded_file(file, category="pet", subcategory="portrait")
    file_hash = file_info["file_hash"]

    # Step 2: Deduplication
    existing = await session.execute(
        select(ProfileUpload).where(ProfileUpload.file_hash == file_hash)
    )
    existing_file = existing.scalar_one_or_none()
    if existing_file:
        if existing_file.user_id != user_id:
            raise PermissionDeniedError("This file belongs to another user.")
        if existing_file.pet_id != pet_id:
            existing_file.pet_id = pet_id
            await session.commit()
        return existing_file

    # Step 3: Ensure pet exists
    await get_pet_profile_service(pet_id, user_id, session)

    # Step 4: Create new record
    new_file = ProfileUpload(
        pet_id=pet_id,
        user_id=user_id,
        **file_info,
        uploaded_at=datetime.utcnow(),
        is_active=True,
    )
    session.add(new_file)
    try:
        await session.commit()
        await session.refresh(new_file)
        return new_file
    except SQLAlchemyError:
        await session.rollback()
        raise InternalError("Failed to upload file. Please try again.")



async def replace_pet_profile_image_service(
    session: AsyncSession,
    file: UploadFile,
    pet_id: int,
    user_id: int,
) -> ProfileUpload:
    # 1) Delete old portrait if it exists
    old = await session.execute(
        select(ProfileUpload).where(
            ProfileUpload.pet_id      == pet_id,
            ProfileUpload.user_id     == user_id,
            ProfileUpload.category    == "pet",
            ProfileUpload.subcategory == "portrait",
        )
    )
    old_file = old.scalar_one_or_none()
    if old_file:
        await session.delete(old_file)
        await session.commit()

    # 2) Delegate to the add‐style logic
    file_info = await save_uploaded_file(file, category="pet", subcategory="portrait")
    file_hash = file_info["file_hash"]

    existing = await session.execute(
        select(ProfileUpload).where(ProfileUpload.file_hash == file_hash)
    )
    existing_file = existing.scalar_one_or_none()
    if existing_file:
        if existing_file.user_id != user_id:
            raise PermissionDeniedError("This file belongs to another user.")
        if existing_file.pet_id != pet_id:
            existing_file.pet_id = pet_id
            await session.commit()
        return existing_file

    # Ensure the pet exists
    await get_pet_profile_service(pet_id, user_id, session)

    new_file = ProfileUpload(
        pet_id=pet_id,
        user_id=user_id,
        **file_info,
        uploaded_at=datetime.utcnow(),
        is_active=True,
    )
    session.add(new_file)
    try:
        await session.commit()
        await session.refresh(new_file)
        return new_file
    except SQLAlchemyError:
        await session.rollback()
        raise InternalError("Failed to replace file. Please try again.")


async def show_pet_data_service(
    pet_id: int,
    parent_id: int,
    session: AsyncSession
) -> PetData:
    result = await session.execute(
        select(PetData)
        .join(Pets, PetData.pet_id == Pets.id)
        .where(PetData.pet_id == pet_id, Pets.parent_id == parent_id)
    )
    pet_data = result.scalar_one_or_none()
    if not pet_data:
        raise NotFoundError("Pet not found or access denied.")
    return pet_data


async def add_pet_data_service(
    pet_id: int, user_id: int, data: PetDataAddSchema, session: AsyncSession
) -> PetData:
    # Verify pet exists & owner
    result = await session.execute(
        select(Pets).where(Pets.id == pet_id, Pets.parent_id == user_id)
    )
    pet = result.scalar_one_or_none()
    if not pet:
        raise NotFoundError("Pet not found or access denied.")

    new_data = PetData(pet_id=pet_id, user_id=user_id, **data.dict())
    session.add(new_data)
    try:
        await session.commit()
        await session.refresh(new_data)
        return new_data
    except SQLAlchemyError:
        await session.rollback()
        raise InternalError("Failed to add pet data. Try again later.")


async def edit_pet_data_service(
    pet_id: int, user_id: int, data: PetDataEditSchema, session: AsyncSession
) -> PetData:
    # Verify pet exists & owner
    result = await session.execute(
        select(Pets).where(Pets.id == pet_id, Pets.parent_id == user_id)
    )
    pet = result.scalar_one_or_none()
    if not pet:
        raise NotFoundError("Pet not found or access denied.")

    # Fetch or create PetData
    result = await session.execute(select(PetData).where(PetData.pet_id == pet_id))
    pet_data = result.scalar_one_or_none() or PetData(pet_id=pet_id, user_id=user_id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(pet_data, field, value or "")

    session.add(pet_data)
    try:
        await session.commit()
        await session.refresh(pet_data)
        return pet_data
    except SQLAlchemyError:
        await session.rollback()
        raise InternalError("Failed to update pet data. Try again later.")



# Helper checks
def is_pet_data_empty(data: PetData) -> bool:
    return all(not getattr(data, f) for f in (
        "favorite_things", "dislikes", "social_style", "communication",
        "preferred_treats", "diet", "allergies", "medical_alerts",
        "behavior_notes", "additional_info"
    ))

def is_pet_profile_empty(pet: Pets) -> bool:
    return all(not getattr(pet, attr) for attr in (
        "birthday", "birth_year", "birth_month", "subspecies",
        "gender", "profile_image_id", "profile_description"
    ))



async def delete_pet_profile_service(
    pet_id: int, user_id: int, session: AsyncSession
):
    # Verify pet + ownership
    result = await session.execute(select(Pets).where(Pets.id == pet_id))
    pet = result.scalar_one_or_none()
    if not pet or pet.parent_id != user_id:
        raise NotFoundError("Pet not found or access denied.")

    # Check PetData
    result = await session.execute(select(PetData).where(PetData.pet_id == pet_id))
    pet_data = result.scalar_one_or_none()
    if pet_data and not is_pet_data_empty(pet_data):
        raise ConflictError("Cannot delete pet — pet data is not empty.")

    # Check profile emptiness
    if not is_pet_profile_empty(pet):
        raise ConflictError("Cannot delete pet — profile still contains data.")

    # Delete medical-related entries
    for model in (VetVisit, VaccinationRecord, MedicalDocument):
        await session.execute(delete(model).where(model.pet_id == pet_id))
    # Delete MedicalProfile
    await session.execute(delete(MedicalProfile).where(MedicalProfile.pet_id == pet_id))
    # Delete PetData
    if pet_data:
        await session.execute(delete(PetData).where(PetData.pet_id == pet_id))
    # Delete the Pet
    await session.execute(delete(Pets).where(Pets.id == pet_id))

    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise InternalError("Failed to delete pet. Try again later.")



async def delete_pet_data_service(
    pet_id: int, user_id: int, session: AsyncSession
):
    # Verify pet + ownership
    result = await session.execute(select(Pets).where(Pets.id == pet_id))
    pet = result.scalar_one_or_none()
    if not pet or pet.parent_id != user_id:
        raise NotFoundError("Pet not found or access denied.")

    # Fetch PetData
    result = await session.execute(select(PetData).where(PetData.pet_id == pet_id))
    pet_data = result.scalar_one_or_none()
    if not pet_data:
        raise NotFoundError("Pet data not found.")

    await session.delete(pet_data)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise InternalError("Failed to delete pet data. Try again later.")

