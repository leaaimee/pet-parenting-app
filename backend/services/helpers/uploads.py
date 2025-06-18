# services/uploads.py
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.domain.exceptions import PermissionDeniedError
from backend.models.media_models import ProfileUpload
from backend.utils.upload_helper import save_uploaded_file
from backend.domain.exceptions import InternalError

from fastapi import UploadFile

from backend.utils.upload_helper import (
    save_uploaded_file,
    VALID_UPLOAD_CATEGORIES,
    VALID_SUBCATEGORIES,
    get_upload_subpath,
    generate_file_hash,
)



async def save_user_avatar(file, session, user_id):
    return await save_file_to_model(
        session=session,
        file=file,
        model=ProfileUpload,
        category="user",
        subcategory="avatar",
        user_id=user_id,
    )


async def save_file_to_model(
    session: AsyncSession,
    file: UploadFile,
    model,            # ProfileUpload or MedicalDocument
    category: str,    # "pet", "user", or "medical"
    subcategory: str, # validate against VALID_SUBCATEGORIES[category]
    **fk_kwargs,
):
    # Validate subcategory up front
    if subcategory not in VALID_SUBCATEGORIES[category]:
        raise ValueError(f"Invalid subcategory '{subcategory}' for category '{category}'")

    # Step 1: Save the file bytes & metadata
    file_info = await save_uploaded_file(file, category, subcategory)
    file_hash = file_info["file_hash"]

    # 2) Deduplication: see if this hash already exists
    result = await session.execute(select(model).where(model.file_hash == file_hash))
    existing = result.scalar_one_or_none()
    if existing:
        # Only the owner can reassign
        if existing.user_id != fk_kwargs.get("user_id"):
            raise PermissionDeniedError("This file belongs to another user.")
        # Re‐parent if needed
        if existing.pet_id != fk_kwargs.get("pet_id"):
            existing.pet_id = fk_kwargs["pet_id"]
            await session.commit()
        return existing

    # 3) Optionally verify the pet (or user) exists before creating
    if "pet_id" in fk_kwargs:
        from backend.services.pets_service import get_pet_profile_service
        await get_pet_profile_service(fk_kwargs["pet_id"], fk_kwargs.get("user_id"), session)

    # 4) Create a new record
    new_file = model(**fk_kwargs, **file_info)
    session.add(new_file)
    try:
        await session.commit()
        await session.refresh(new_file)
        return new_file
    except SQLAlchemyError:
        await session.rollback()
        raise InternalError("Failed to upload file. Try again later.")